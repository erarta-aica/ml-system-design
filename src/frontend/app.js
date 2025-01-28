class FoodCalorieUI {
    constructor() {
        this.dropZone = document.getElementById('drop-zone');
        this.setupEventListeners();
        this.setupCache();
        
        // API ключ можно хранить в переменных окружения или получать с бэкенда
        this.OPENAI_API_KEY = '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'; // В реальном приложении не храните ключ в коде!
    }

    setupCache() {
        this.cache = new Map();
        // Ограничиваем размер кэша
        setInterval(() => this.cleanCache(), 1000 * 60 * 60); // Каждый час
    }

    setupEventListeners() {
        // Предотвращаем стандартное поведение браузера при drag&drop
        ['dragenter', 'dragover', 'dragleave', 'drop'].forEach(eventName => {
            this.dropZone.addEventListener(eventName, (e) => {
                e.preventDefault();
                e.stopPropagation();
            });
        });

        // Добавляем визуальный эффект при перетаскивании
        ['dragenter', 'dragover'].forEach(eventName => {
            this.dropZone.addEventListener(eventName, () => {
                this.dropZone.classList.add('dragover');
            });
        });

        ['dragleave', 'drop'].forEach(eventName => {
            this.dropZone.addEventListener(eventName, () => {
                this.dropZone.classList.remove('dragover');
            });
        });

        // Обработка сброшенного файла
        this.dropZone.addEventListener('drop', (e) => {
            const file = e.dataTransfer.files[0];
            if (file) {
                this.handleFile(file);
            }
        });

        // Обработка клика
        this.dropZone.addEventListener('click', () => {
            const input = document.createElement('input');
            input.type = 'file';
            input.accept = 'image/*';
            input.onchange = (e) => {
                const file = e.target.files[0];
                if (file) {
                    this.handleFile(file);
                }
            };
            input.click();
        });
    }

    async handleFile(file) {
        try {
            this.showLoading();
            
            // Проверяем кэш
            const cacheKey = await this.calculateHash(file);
            if (this.cache.has(cacheKey)) {
                this.displayResults(this.cache.get(cacheKey));
                return;
            }

            // Конвертируем файл в base64
            const base64Image = await this.fileToBase64(file);
            
            // Отправляем запрос к ChatGPT
            const result = await this.analyzeFoodImage(base64Image);
            
            // Сохраняем в кэш
            this.cache.set(cacheKey, result);
            
            this.displayResults(result);
        } catch (error) {
            this.showError(error);
        } finally {
            this.hideLoading();
        }
    }

    async calculateHash(file) {
        const buffer = await file.arrayBuffer();
        const hashBuffer = await crypto.subtle.digest('SHA-256', buffer);
        return Array.from(new Uint8Array(hashBuffer))
            .map(b => b.toString(16).padStart(2, '0'))
            .join('');
    }

    async fileToBase64(file) {
        return new Promise((resolve, reject) => {
            const reader = new FileReader();
            reader.onload = () => resolve(reader.result.split(',')[1]);
            reader.onerror = reject;
            reader.readAsDataURL(file);
        });
    }

    async analyzeFoodImage(base64Image) {
        const response = await fetch('https://api.openai.com/v1/chat/completions', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'Authorization': `Bearer ${this.OPENAI_API_KEY}`
            },
            body: JSON.stringify({
                model: "gpt-4-vision-preview",
                messages: [
                    {
                        role: "user",
                        content: [
                            {
                                type: "text",
                                text: "Analyze this food image and provide: 1) What food items you see 2) Estimated calories for the entire portion. Return the result in JSON format with fields: foodItems (array of strings) and totalCalories (number)"
                            },
                            {
                                type: "image_url",
                                image_url: {
                                    url: `data:image/jpeg;base64,${base64Image}`
                                }
                            }
                        ]
                    }
                ],
                max_tokens: 500
            })
        });

        if (!response.ok) {
            throw new Error('Failed to analyze image');
        }

        const data = await response.json();
        try {
            // Парсим JSON из текстового ответа
            const result = JSON.parse(data.choices[0].message.content);
            return result;
        } catch (e) {
            // Если не удалось распарсить JSON, возвращаем текст как есть
            return {
                foodItems: ["Could not parse items"],
                totalCalories: 0,
                rawResponse: data.choices[0].message.content
            };
        }
    }

    displayResults(result) {
        const modal = document.createElement('div');
        modal.className = 'result-modal';
        
        const foodItemsList = result.foodItems
            .map(item => `<li>${item}</li>`)
            .join('');

        modal.innerHTML = `
            <div class="modal-content">
                <h2>Food Analysis Results</h2>
                <div class="food-items">
                    <h3>Detected Food Items:</h3>
                    <ul>${foodItemsList}</ul>
                </div>
                <div class="calories">
                    <h3>Estimated Calories:</h3>
                    <p>${result.totalCalories} kcal</p>
                </div>
                <button onclick="this.parentElement.parentElement.remove()">Close</button>
            </div>
        `;
        
        document.body.appendChild(modal);
    }

    showLoading() {
        const loader = document.createElement('div');
        loader.className = 'loader';
        this.dropZone.appendChild(loader);
    }

    hideLoading() {
        const loader = this.dropZone.querySelector('.loader');
        if (loader) loader.remove();
    }

    showError(error) {
        const errorDiv = document.createElement('div');
        errorDiv.className = 'error-message';
        errorDiv.textContent = `Error: ${error.message}`;
        this.dropZone.appendChild(errorDiv);
        setTimeout(() => errorDiv.remove(), 3000);
    }

    cleanCache() {
        const maxCacheAge = 1000 * 60 * 60; // 1 час
        const now = Date.now();
        for (const [key, value] of this.cache.entries()) {
            if (now - value.timestamp > maxCacheAge) {
                this.cache.delete(key);
            }
        }
    }
}

// Инициализация при загрузке страницы
document.addEventListener('DOMContentLoaded', () => {
    new FoodCalorieUI();
}); 