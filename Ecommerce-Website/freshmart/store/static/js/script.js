/* ═══════════════════════════════════════════════════════════
   FRESH MART — MAIN JAVASCRIPT
   ═══════════════════════════════════════════════════════════ */

document.addEventListener('DOMContentLoaded', function () {

    // ─── Navbar Scroll Effect ──────────────────────────────
    const navbar = document.getElementById('navbar');
    const scrollTopBtn = document.querySelector('.scroll-top');

    window.addEventListener('scroll', function () {
        if (window.scrollY > 50) {
            navbar.classList.add('scrolled');
        } else {
            navbar.classList.remove('scrolled');
        }

        // Scroll-to-top button
        if (scrollTopBtn) {
            if (window.scrollY > 400) {
                scrollTopBtn.classList.add('show');
            } else {
                scrollTopBtn.classList.remove('show');
            }
        }
    });

    if (scrollTopBtn) {
        scrollTopBtn.addEventListener('click', function () {
            window.scrollTo({ top: 0, behavior: 'smooth' });
        });
    }

    // ─── Mobile Menu ───────────────────────────────────────
    const mobileMenuToggle = document.getElementById('mobileMenuToggle');
    const mobileMenu = document.getElementById('mobileMenu');
    const closeMobileMenu = document.getElementById('closeMobileMenu');
    const overlay = document.getElementById('overlay');

    function openMobileMenu() {
        mobileMenu.classList.add('show');
        overlay.classList.add('show');
        document.body.style.overflow = 'hidden';
    }

    function closeMobileMenuFn() {
        mobileMenu.classList.remove('show');
        overlay.classList.remove('show');
        document.body.style.overflow = '';
    }

    if (mobileMenuToggle) {
        mobileMenuToggle.addEventListener('click', openMobileMenu);
    }

    if (closeMobileMenu) {
        closeMobileMenu.addEventListener('click', closeMobileMenuFn);
    }

    if (overlay) {
        overlay.addEventListener('click', closeMobileMenuFn);
    }

    // Close mobile menu on link click
    const mobileLinks = document.querySelectorAll('.mobile-menu-links a');
    mobileLinks.forEach(function (link) {
        link.addEventListener('click', closeMobileMenuFn);
    });

    // ─── Search Bar Toggle ─────────────────────────────────
    const searchToggle = document.getElementById('searchToggle');
    const searchBar = document.getElementById('searchBar');

    if (searchToggle && searchBar) {
        searchToggle.addEventListener('click', function () {
            searchBar.classList.toggle('show');
            if (searchBar.classList.contains('show')) {
                searchBar.querySelector('input').focus();
            }
        });
    }

    // ─── User Dropdown ─────────────────────────────────────
    const userToggle = document.getElementById('userToggle');
    const userDropdown = document.getElementById('userDropdown');

    if (userToggle && userDropdown) {
        userToggle.addEventListener('click', function (e) {
            e.stopPropagation();
            userDropdown.classList.toggle('show');
        });

        document.addEventListener('click', function (e) {
            if (!userDropdown.contains(e.target)) {
                userDropdown.classList.remove('show');
            }
        });
    }

    // ─── Auto-hide Messages ────────────────────────────────
    const messageToasts = document.querySelectorAll('.message-toast');
    messageToasts.forEach(function (toast) {
        setTimeout(function () {
            toast.style.animation = 'slideOutRight 0.4s ease';
            setTimeout(function () {
                toast.remove();
            }, 400);
        }, 4000);
    });

    // ─── Smooth Scrolling for Anchor Links ─────────────────
    document.querySelectorAll('a[href^="#"]').forEach(function (anchor) {
        anchor.addEventListener('click', function (e) {
            const href = this.getAttribute('href');
            if (href === '#') return;

            e.preventDefault();
            const target = document.querySelector(href);
            if (target) {
                target.scrollIntoView({
                    behavior: 'smooth',
                    block: 'start'
                });
            }
        });
    });

    // ─── Scroll Animations (Intersection Observer) ─────────
    const observerOptions = {
        threshold: 0.1,
        rootMargin: '0px 0px -50px 0px'
    };

    const observer = new IntersectionObserver(function (entries) {
        entries.forEach(function (entry) {
            if (entry.isIntersecting) {
                entry.target.style.opacity = '1';
                entry.target.style.transform = 'translateY(0)';
                observer.unobserve(entry.target);
            }
        });
    }, observerOptions);

    document.querySelectorAll('.product-card, .feature-card, .testimonial-card, .category-card, .order-card').forEach(function (el) {
        el.style.opacity = '0';
        el.style.transform = 'translateY(30px)';
        el.style.transition = 'all 0.6s ease';
        observer.observe(el);
    });

    // ─── Add to Cart (AJAX) ────────────────────────────────
    const addToCartForms = document.querySelectorAll('.add-to-cart-form, .btn-add-to-cart');

    document.querySelectorAll('.add-to-cart-form').forEach(function (form) {
        form.addEventListener('submit', function (e) {
            e.preventDefault();

            const formData = new FormData(this);
            const url = this.getAttribute('action');

            fetch(url, {
                method: 'POST',
                body: formData,
                headers: {
                    'X-Requested-With': 'XMLHttpRequest',
                    'X-CSRFToken': formData.get('csrfmiddlewaretoken')
                }
            })
            .then(function (response) { return response.json(); })
            .then(function (data) {
                if (data.success) {
                    // Update cart count
                    const cartCountEl = document.querySelector('.cart-count');
                    if (cartCountEl) {
                        cartCountEl.textContent = data.cart_count;
                        cartCountEl.style.animation = 'bounce 0.5s ease';
                        setTimeout(function () {
                            cartCountEl.style.animation = '';
                        }, 500);
                    } else {
                        // Add cart count badge if it doesn't exist
                        const cartIcon = document.querySelector('.cart-icon-link');
                        if (cartIcon) {
                            const badge = document.createElement('span');
                            badge.className = 'cart-count';
                            badge.textContent = data.cart_count;
                            cartIcon.appendChild(badge);
                        }
                    }

                    showNotification(data.message, 'success');
                }
            })
            .catch(function () {
                // Fallback: submit normally
                form.submit();
            });
        });
    });

    // ─── Product Detail Add to Cart ────────────────────────
    const detailForm = document.querySelector('.add-to-cart-detail-form');
    if (detailForm) {
        detailForm.addEventListener('submit', function (e) {
            e.preventDefault();

            const formData = new FormData(this);
            const url = this.getAttribute('action');

            fetch(url, {
                method: 'POST',
                body: formData,
                headers: {
                    'X-Requested-With': 'XMLHttpRequest',
                    'X-CSRFToken': formData.get('csrfmiddlewaretoken')
                }
            })
            .then(function (response) { return response.json(); })
            .then(function (data) {
                if (data.success) {
                    const cartCountEl = document.querySelector('.cart-count');
                    if (cartCountEl) {
                        cartCountEl.textContent = data.cart_count;
                    }
                    showNotification(data.message, 'success');
                }
            })
            .catch(function () {
                detailForm.submit();
            });
        });
    }

    // ─── Quantity Selector on Product Detail ───────────────
    const qtyMinus = document.querySelector('.qty-minus');
    const qtyPlus = document.querySelector('.qty-plus');
    const qtyInput = document.querySelector('.qty-input');

    if (qtyMinus && qtyPlus && qtyInput) {
        qtyMinus.addEventListener('click', function () {
            let val = parseInt(qtyInput.value);
            if (val > 1) qtyInput.value = val - 1;
        });
        qtyPlus.addEventListener('click', function () {
            let val = parseInt(qtyInput.value);
            let max = parseInt(qtyInput.getAttribute('max')) || 99;
            if (val < max) qtyInput.value = val + 1;
        });
    }

    // ─── Payment Option Selection ──────────────────────────
    const paymentOptions = document.querySelectorAll('.payment-option');
    paymentOptions.forEach(function (option) {
        option.addEventListener('click', function () {
            paymentOptions.forEach(function (o) { o.classList.remove('selected'); });
            this.classList.add('selected');
            this.querySelector('input').checked = true;
        });
    });

    // ─── Newsletter Form ───────────────────────────────────
    const newsletterForm = document.getElementById('newsletterForm');
    if (newsletterForm) {
        newsletterForm.addEventListener('submit', function (e) {
            e.preventDefault();
            const email = newsletterForm.querySelector('input[type="email"]').value;
            showNotification('Thanks for subscribing! We\'ll send updates to ' + email, 'success');
            newsletterForm.reset();
        });
    }

    // ─── Image Preview for Product Upload ──────────────────
    const imageInput = document.querySelector('input[type="file"]');
    if (imageInput) {
        imageInput.addEventListener('change', function (e) {
            const file = e.target.files[0];
            if (file) {
                const reader = new FileReader();
                reader.onload = function (event) {
                    let preview = document.querySelector('.image-preview');
                    if (!preview) {
                        preview = document.createElement('img');
                        preview.className = 'image-preview';
                        preview.style.maxWidth = '200px';
                        preview.style.borderRadius = '8px';
                        preview.style.marginTop = '10px';
                        imageInput.parentNode.appendChild(preview);
                    }
                    preview.src = event.target.result;
                };
                reader.readAsDataURL(file);
            }
        });
    }

    // ─── Confirm Delete Actions ────────────────────────────
    document.querySelectorAll('.confirm-delete').forEach(function (btn) {
        btn.addEventListener('click', function (e) {
            if (!confirm('Are you sure you want to remove this item?')) {
                e.preventDefault();
            }
        });
    });

    // ─── Form Validation Enhancement ───────────────────────
    document.querySelectorAll('form').forEach(function (form) {
        form.addEventListener('submit', function () {
            const submitBtn = form.querySelector('button[type="submit"]');
            if (submitBtn) {
                submitBtn.disabled = true;
                const originalText = submitBtn.innerHTML;
                submitBtn.innerHTML = '<i class="fas fa-spinner fa-spin"></i> Processing...';
                
                // Re-enable after 5 seconds in case of error
                setTimeout(function () {
                    submitBtn.disabled = false;
                    submitBtn.innerHTML = originalText;
                }, 5000);
            }
        });
    });

});

// ─── Notification Function ────────────────────────────────
function showNotification(message, type) {
    type = type || 'success';
    const container = document.querySelector('.messages-container') || createMessagesContainer();
    
    const toast = document.createElement('div');
    toast.className = 'message-toast message-' + type;
    toast.innerHTML = '<span class="message-text">' + message + '</span>' +
                      '<button class="message-close" onclick="this.parentElement.remove()">&times;</button>';
    
    container.appendChild(toast);

    setTimeout(function () {
        toast.style.animation = 'slideOutRight 0.4s ease';
        setTimeout(function () {
            toast.remove();
        }, 400);
    }, 4000);
}

function createMessagesContainer() {
    const container = document.createElement('div');
    container.className = 'messages-container';
    document.body.appendChild(container);
    return container;
}

// ─── Delete Confirmation ──────────────────────────────────
function confirmAction(message) {
    return confirm(message || 'Are you sure?');
}

// Close mobile menu on link click
// const mobileLinks = document.querySelectorAll('.mobile-menu-links a');
// mobileLinks.forEach(function (link) {
//     link.addEventListener('click', function () {
//         document.getElementById('mobileMenu').classList.remove('show');
//         document.getElementById('overlay').classList.remove('show');
//         document.body.style.overflow = '';
//     });
// });