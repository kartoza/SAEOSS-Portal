document.addEventListener('DOMContentLoaded', function() {
    const carouselItems = document.querySelectorAll('.carousel-item');
    const dots = document.querySelectorAll('.carousel-dot');
    const prevBtn = document.querySelector('.carousel-btn.prev');
    const nextBtn = document.querySelector('.carousel-btn.next');
    let currentIndex = 0;
    
    function updateCarousel(index) {
        carouselItems.forEach(item => item.classList.remove('active'));
        dots.forEach(dot => dot.classList.remove('active'));
        
        carouselItems[index].classList.add('active');
        dots[index].classList.add('active');
        
        currentIndex = index;
    }
    
    nextBtn.addEventListener('click', function() {
        let nextIndex = (currentIndex + 1) % carouselItems.length;
        updateCarousel(nextIndex);
    });
    
    prevBtn.addEventListener('click', function() {
        let prevIndex = (currentIndex - 1 + carouselItems.length) % carouselItems.length;
        updateCarousel(prevIndex);
    });
    
    dots.forEach(dot => {
        dot.addEventListener('click', function() {
            const index = parseInt(this.getAttribute('data-index'));
            updateCarousel(index);
        });
    });
    
    let autoSlide = setInterval(() => {
        let nextIndex = (currentIndex + 1) % carouselItems.length;
        updateCarousel(nextIndex);
    }, 5000);
    
    const carouselContainer = document.querySelector('.carousel-container');
    carouselContainer.addEventListener('mouseenter', () => {
        clearInterval(autoSlide);
    });
    
    carouselContainer.addEventListener('mouseleave', () => {
        autoSlide = setInterval(() => {
            let nextIndex = (currentIndex + 1) % carouselItems.length;
            updateCarousel(nextIndex);
        }, 5000);
    });
    
    window.addEventListener('scroll', function() {
        const navbar = document.querySelector('.navbar');
        if (window.scrollY > 50) {
            navbar.classList.add('scrolled');
        } else {
            navbar.classList.remove('scrolled');
        }
    });
});