class FoodCalorieUI {
    constructor() {
        this.dropZone = document.getElementById('drop-zone');
        this.setupEventListeners();
        this.setupCache();
        
        // Базовый URL для GitHub Pages
        this.baseUrl = '/ml-system-design';
    }

    setupCache() {
        this.cache = new Map();
        // Ограничиваем размер кэша
        setInterval(() => this.cleanCache(), 1000 * 60 * 60); // Каждый час
    }

    setupEventListeners() {
        this.dropZone.addEventListener('dragover', (e) => {
            e.preventDefault();
            this.dropZone.classList.add('dragover');
        });

        this.dropZone.addEventListener('dragleave', () => {
            this.dropZone.classList.remove('dragover');
        });

        this.dropZone.addEventListener('drop', async (e) => {
            e.preventDefault();
            this.dropZone.classList.remove('dragover');
            const file = e.dataTransfer.files[0];
            await this.handleFile(file);
        });

        // Добавляем поддержку клика
        this.dropZone.addEventListener('click', () => {
            const input = document.createElement('input');
            input.type = 'file';
            input.accept = 'image/*';
            input.onchange = (e) => this.handleFile(e.target.files[0]);
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

            const formData = new FormData();
            formData.append('image', file);

            const response = await fetch('https://your-huggingface-space-url/api/predict', {
                method: 'POST',
                body: formData
            });

            const result = await response.json();
            
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

    displayResults(result) {
        // Создаем и показываем модальное окно с результатами
        const modal = document.createElement('div');
        modal.className = 'result-modal';
        modal.innerHTML = `
            <div class="modal-content">
                <h2>Results</h2>
                <p>Estimated calories: ${result.calories.toFixed(0)} kcal</p>
                <button onclick="this.parentElement.remove()">Close</button>
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