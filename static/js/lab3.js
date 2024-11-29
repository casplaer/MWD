document.addEventListener("DOMContentLoaded", function () {
    let carousel = document.querySelector(".carousel");
    let items = carousel.querySelectorAll(".item");
    let dotsContainer = document.querySelector(".dots");
    const currentTime = new Date().getTime();

    const tableHeaders = document.querySelectorAll('th');
    
    tableHeaders.forEach((header, index) => {
        header.addEventListener('click', () => sortTable(index));
    });

    let sessionStartTime = localStorage.getItem('sessionStartTime');

    const countdownDuration = 60 * 60 * 1000;

    const timeRemaining = countdownDuration - (currentTime - sessionStartTime);

    setInterval(updateTimer, 1000);

    function updateTimer() {
        const now = new Date().getTime();
        const remainingTime = countdownDuration - (now - sessionStartTime);

        if (remainingTime <= 0) {
            document.getElementById("countdown-timer").innerHTML = "<p>Время вышло!</p>";
            localStorage.removeItem('sessionStartTime');
        } else {
            const hours = Math.floor(remainingTime / (1000 * 60 * 60));
            const minutes = Math.floor((remainingTime % (1000 * 60 * 60)) / (1000 * 60));
            const seconds = Math.floor((remainingTime % (1000 * 60)) / 1000);

            document.getElementById("timer").innerHTML = `${hours}ч ${minutes}м ${seconds}с`;
        }
    }

    if (!sessionStartTime) {
        sessionStartTime = currentTime;
        localStorage.setItem('sessionStartTime', sessionStartTime);
    }

    if (sliderSettings.pags) {
        items.forEach((_, index) => {
            let dot = document.createElement("span");
            dot.classList.add("dot");
            if (index === 0) dot.classList.add("active");
            dot.dataset.index = index;
            dotsContainer.appendChild(dot);
        });
    } else {
        dotsContainer.style.display = "none";
    }

    let dots = document.querySelectorAll(".dot");

    function showItem(index) {
        items.forEach((item, idx) => {
            item.classList.remove("active");
            dots[idx]?.classList.remove("active");
            if (idx === index) {
                item.classList.add("active");
                dots[idx]?.classList.add("active");
            }
        });
    }

    let currentIndex = 0;
    
    function autoSlide() {
        if (sliderSettings.auto) {
            if (sliderSettings.loop) {
                currentIndex = (currentIndex + 1) % items.length; 
            } else if (currentIndex < items.length - 1) {
                currentIndex++;
            }
            showItem(currentIndex);
        }
    }

    let slideInterval;
    if (sliderSettings.auto) {
        slideInterval = setInterval(autoSlide, sliderSettings.delay * 1000 || 5000); 
    }

    if (sliderSettings.stopMouseHover) {
        carousel.addEventListener("mouseenter", () => {
            clearInterval(slideInterval);
        });

        carousel.addEventListener("mouseleave", () => {
            slideInterval = setInterval(autoSlide, sliderSettings.delay * 1000 || 5000);
        });
    }

    if (sliderSettings.navs) {
        document.querySelector(".prev").addEventListener("click", () => {
            if (sliderSettings.loop || currentIndex > 0) {
                currentIndex = (currentIndex - 1 + items.length) % items.length;
                showItem(currentIndex);
            }
        });

        document.querySelector(".next").addEventListener("click", () => {
            if (sliderSettings.loop || currentIndex < items.length - 1) {
                currentIndex = (currentIndex + 1) % items.length;
                showItem(currentIndex);
            }
        });
    } else {
        const navButtons = document.querySelectorAll(".btn");
        navButtons.forEach((btn) => btn.style.display = "none");
    }

    if (sliderSettings.pags) {
        dots.forEach((dot) => {
            dot.addEventListener("click", () => {
                let index = parseInt(dot.dataset.index);
                currentIndex = index;
                showItem(index);
            });
        });
    }

    showItem(0); 

    let sortOrder = {
        title: null,
        description: null,
        phone_number: null,
        email: null
    };
    
    console.log('sortTable loaded')

    function sortTable(columnIndex) {
        const table = document.getElementById("contactsTable");
        const rows = Array.from(table.rows).slice(1);
        const columnName = table.rows[0].cells[columnIndex].getAttribute('data-column');
        
        const currentSortOrder = sortOrder[columnName];
        const newSortOrder = currentSortOrder === 'asc' ? 'desc' : 'asc';
        
        rows.sort((a, b) => {
            const cellA = a.cells[columnIndex].innerText;
            const cellB = b.cells[columnIndex].innerText;
    
            let comparison = 0;
            
            if (cellA < cellB) {
                console.log("123123");
                comparison = -1;
            } else if (cellA > cellB) {
                comparison = 1;
            }
    
            return newSortOrder === 'asc' ? comparison : -comparison;
        });
    
        rows.forEach(row => table.appendChild(row));
    
        sortOrder[columnName] = newSortOrder;
    
        updateSortIndicators(columnIndex, newSortOrder);
    }
    
    function updateSortIndicators(columnIndex, newSortOrder) {
        const headers = document.querySelectorAll('th');
        
        headers.forEach(header => {
            header.classList.remove('sorted-asc', 'sorted-desc');
        });
    
        headers[columnIndex].classList.add(newSortOrder === 'asc' ? 'sorted-asc' : 'sorted-desc');
    }
    const products = document.querySelectorAll('.product');
    const cart = document.querySelector('.cart');

    // Функция для проверки, видна ли картинка на экране
    function isInView(element) {
        const rect = element.getBoundingClientRect();
        return rect.top <= window.innerHeight && rect.bottom >= 0;
    }

    // Функция для анимации падения продуктов
    function animateProducts() {
        products.forEach((product, index) => {
            if (isInView(product)) {
                // Вычисляем начальную позицию падения
                const distanceToCart = cart.getBoundingClientRect().top - product.getBoundingClientRect().top;

                // Делаем продукт видимым, убираем его начальную непрозрачность
                product.style.opacity = 1;

                // Делаем анимацию падения через изменение вертикальной позиции
                product.style.transition = 'transform 2s ease-in-out';
                product.style.transform = `translateY(${distanceToCart}px)`;
            } else {
                // Продукт скрывается, если он не виден
                product.style.opacity = 0;
                product.style.transform = 'translateY(0)';
            }
        });
    }

    // Слушаем событие прокрутки
    window.addEventListener('scroll', animateProducts);

    // Начальная анимация продуктов
    animateProducts();
});

