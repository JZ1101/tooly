// Landing page interactions
document.addEventListener('DOMContentLoaded', function() {
    // Smooth scrolling for navigation links
    const links = document.querySelectorAll('a[href^="#"]');
    links.forEach(link => {
        link.addEventListener('click', function(e) {
            e.preventDefault();
            const target = document.querySelector(this.getAttribute('href'));
            if (target) {
                target.scrollIntoView({
                    behavior: 'smooth',
                    block: 'start'
                });
            }
        });
    });

    // Add scroll effect to navigation
    let lastScrollTop = 0;
    const nav = document.querySelector('.nav');
    
    window.addEventListener('scroll', function() {
        let scrollTop = window.pageYOffset || document.documentElement.scrollTop;
        
        if (scrollTop > lastScrollTop && scrollTop > 100) {
            // Scrolling down
            nav.style.transform = 'translateY(-100%)';
        } else {
            // Scrolling up
            nav.style.transform = 'translateY(0)';
        }
        lastScrollTop = scrollTop;
    });

    // Animate stats when they come into view
    const observeStats = new IntersectionObserver((entries) => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                const statNumbers = entry.target.querySelectorAll('.stat-number');
                statNumbers.forEach(stat => {
                    animateNumber(stat);
                });
                observeStats.unobserve(entry.target);
            }
        });
    });

    const statsSection = document.querySelector('.hero-stats');
    if (statsSection) {
        observeStats.observe(statsSection);
    }

    // Animate feature cards
    const observeCards = new IntersectionObserver((entries) => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                entry.target.style.opacity = '1';
                entry.target.style.transform = 'translateY(0)';
            }
        });
    }, {
        threshold: 0.1
    });

    const featureCards = document.querySelectorAll('.feature-card');
    featureCards.forEach(card => {
        card.style.opacity = '0';
        card.style.transform = 'translateY(20px)';
        card.style.transition = 'opacity 0.6s, transform 0.6s';
        observeCards.observe(card);
    });

    // Demo chat animation
    setTimeout(() => {
        animateDemoChat();
    }, 2000);
});

function animateNumber(element) {
    const target = parseInt(element.textContent);
    const isPercentage = element.textContent.includes('%');
    const isPlusSign = element.textContent.includes('+');
    
    let current = 0;
    const increment = target / 30;
    const timer = setInterval(() => {
        current += increment;
        if (current >= target) {
            current = target;
            clearInterval(timer);
        }
        
        let displayValue = Math.floor(current);
        if (isPercentage) displayValue += '%';
        if (isPlusSign && displayValue === target) displayValue += '+';
        
        element.textContent = displayValue;
    }, 50);
}

function animateDemoChat() {
    const messages = document.querySelectorAll('.demo .message');
    let delay = 0;
    
    messages.forEach((message, index) => {
        if (index === 0) return; // Skip first message
        
        message.style.opacity = '0';
        message.style.transform = 'translateY(20px)';
        
        setTimeout(() => {
            message.style.transition = 'opacity 0.5s, transform 0.5s';
            message.style.opacity = '1';
            message.style.transform = 'translateY(0)';
            
            // Scroll to show new message
            const container = message.closest('.chat-messages');
            if (container) {
                container.scrollTop = container.scrollHeight;
            }
        }, delay);
        
        delay += 2000; // 2 second delay between messages
    });
}