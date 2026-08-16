document.addEventListener('DOMContentLoaded', () => {

    const hasAnime = typeof anime !== 'undefined';
    const hasGSAP = typeof gsap !== 'undefined' && typeof ScrollTrigger !== 'undefined';
    const hasLenis = typeof Lenis !== 'undefined';
    const hasThree = typeof THREE !== 'undefined';

    // ===================================================
    // 0. THREE.JS WEBGL AMBIENT PARTICLE BACKGROUND
    // ===================================================
    if (hasThree) {
        const canvas = document.getElementById('webgl-canvas');
        if (canvas) {
            const scene = new THREE.Scene();
            const camera = new THREE.PerspectiveCamera(75, window.innerWidth / window.innerHeight, 0.1, 1000);
            const renderer = new THREE.WebGLRenderer({ canvas, alpha: true, antialias: true });
            
            renderer.setSize(window.innerWidth, window.innerHeight);
            renderer.setPixelRatio(Math.min(window.devicePixelRatio, 2));

            const particlesCount = 180;
            const geometry = new THREE.BufferGeometry();
            const positions = new Float32Array(particlesCount * 3);
            const colors = new Float32Array(particlesCount * 3);

            for (let i = 0; i < particlesCount * 3; i += 3) {
                positions[i] = (Math.random() - 0.5) * 14;
                positions[i+1] = (Math.random() - 0.5) * 14;
                positions[i+2] = (Math.random() - 0.5) * 14;

                // Gold / Champagne ambient RGB
                colors[i] = 0.77;   
                colors[i+1] = 0.61; 
                colors[i+2] = 0.42; 
            }

            geometry.setAttribute('position', new THREE.BufferAttribute(positions, 3));
            geometry.setAttribute('color', new THREE.BufferAttribute(colors, 3));

            const material = new THREE.PointsMaterial({
                size: 0.045,
                vertexColors: true,
                transparent: true,
                opacity: 0.45,
                blending: THREE.AdditiveBlending
            });

            const particlesMesh = new THREE.Points(geometry, material);
            scene.add(particlesMesh);
            camera.position.z = 5;

            let targetMouseX = 0;
            let targetMouseY = 0;

            window.addEventListener('mousemove', (e) => {
                targetMouseX = (e.clientX / window.innerWidth) - 0.5;
                targetMouseY = (e.clientY / window.innerHeight) - 0.5;
            });

            function animateWebGL() {
                requestAnimationFrame(animateWebGL);
                particlesMesh.rotation.y += 0.0012;
                particlesMesh.rotation.x += 0.0008;

                camera.position.x += (targetMouseX * 0.6 - camera.position.x) * 0.04;
                camera.position.y += (-targetMouseY * 0.6 - camera.position.y) * 0.04;

                renderer.render(scene, camera);
            }
            animateWebGL();

            window.addEventListener('resize', () => {
                camera.aspect = window.innerWidth / window.innerHeight;
                camera.updateProjectionMatrix();
                renderer.setSize(window.innerWidth, window.innerHeight);
            });
        }
    }

    // ===================================================
    // LIVE TICKING IST CLOCK
    // ===================================================
    function updateLiveClock() {
        const clockEl = document.getElementById('live-clock');
        if (clockEl) {
            const now = new Date();
            const options = { timeZone: 'Asia/Kolkata', hour12: false, hour: '2-digit', minute: '2-digit', second: '2-digit' };
            clockEl.textContent = now.toLocaleTimeString('en-US', options) + ' IST';
        }
    }
    setInterval(updateLiveClock, 1000);
    updateLiveClock();

    // ===================================================
    // LENIS INERTIA SMOOTH SCROLL
    // ===================================================
    let lenis = null;
    const isMobile = window.innerWidth < 768;
    if (hasLenis) {
        lenis = new Lenis({
            duration: isMobile ? 1.0 : 1.4,
            easing: (t) => Math.min(1, 1.001 - Math.pow(2, -10 * t)),
            smoothWheel: true,
            wheelMultiplier: isMobile ? 0.8 : 1.15,
            touchMultiplier: isMobile ? 0.6 : 1.8
        });

        function raf(time) {
            lenis.raf(time);
            requestAnimationFrame(raf);
        }
        requestAnimationFrame(raf);

        if (hasGSAP) {
            lenis.on('scroll', ScrollTrigger.update);
            gsap.ticker.add((time) => {
                lenis.raf(time * 1000);
            });
            gsap.ticker.lagSmoothing(0);
        }
    }

    // ===================================================
    // MULTI-STATE FLUID MAGNETIC CURSOR (Active Theory / Ricardo Chance)
    // ===================================================
    const dot = document.querySelector('.cursor-dot');
    const ring = document.querySelector('.cursor-ring');
    const cursorLabel = document.querySelector('.cursor-label');

    if (dot && ring && window.innerWidth >= 992) {
        let mouseX = window.innerWidth / 2;
        let mouseY = window.innerHeight / 2;
        let ringX = mouseX;
        let ringY = mouseY;

        window.addEventListener('mousemove', (e) => {
            mouseX = e.clientX;
            mouseY = e.clientY;
            dot.style.transform = `translate(${mouseX}px, ${mouseY}px) translate(-50%, -50%)`;
        });

        function animateRing() {
            ringX += (mouseX - ringX) * 0.18;
            ringY += (mouseY - ringY) * 0.18;
            ring.style.transform = `translate(${ringX}px, ${ringY}px) translate(-50%, -50%)`;
            requestAnimationFrame(animateRing);
        }
        animateRing();

        // Multi-state cursor labels
        const cursorTargets = [
            { selector: '.btn-hero, .btn-dark-pill, .btn-nav-cta, .btn-book-sm', label: 'BOOK' },
            { selector: '.p-card-img, .pc-img, .t-card-img', label: 'VIEW' },
            { selector: '.marquee-card', label: 'PROOF' },
            { selector: 'a[href^="#"]', label: 'JUMP' },
            { selector: 'input', label: 'TYPE' }
        ];

        cursorTargets.forEach(group => {
            document.querySelectorAll(group.selector).forEach(item => {
                item.addEventListener('mouseenter', () => {
                    if (cursorLabel) cursorLabel.textContent = group.label;
                    document.body.classList.add('cursor-hover');
                });
                item.addEventListener('mouseleave', () => {
                    document.body.classList.remove('cursor-hover');
                });
            });
        });
    }

    // ===================================================
    // IMAGE REVEAL OBSERVER
    // ===================================================
    document.querySelectorAll('.hero-img-card img, .about-heading img, .p-card-img img, .pc-img img').forEach(img => {
        img.classList.add('img-mask-reveal', 'revealed');
    });

    // ===================================================
    // GSAP SCROLLTRIGGER 3D STORYTELLING SEQUENCE
    // ===================================================
    if (hasGSAP) {
        gsap.registerPlugin(ScrollTrigger);

        // A. Pinned 3D Hero Storytelling Sequence (Desktop only)
        if (window.innerWidth > 768) {
            const heroTl = gsap.timeline({
                scrollTrigger: {
                    trigger: ".hero-section",
                    start: "top top",
                    end: "+=100%",
                    scrub: 1,
                    pin: true,
                    anticipatePin: 1
                }
            });

        // Step 1: Hero left text rotates and recedes into 3D depth
        heroTl.to(".hero-left", {
            rotateX: 20,
            rotateY: -12,
            z: -180,
            opacity: 0.2,
            ease: "power2.inOut"
        }, 0);

        // Step 2: Hero Image Card expands & rotates to 3D center stage
        heroTl.to(".hero-img-card", {
            scale: 1.12,
            rotateY: -6,
            rotateX: 4,
            z: 120,
            boxShadow: "0 60px 120px rgba(0,0,0,0.7)",
            ease: "power2.inOut"
        }, 0);

        // Step 3: 3D Floating Badges fly out into 3D foreground depth
        heroTl.to(".badge-top-left", {
            x: -80,
            y: -40,
            z: 200,
            scale: 1.25,
            ease: "power2.out"
        }, 0.2);

        heroTl.to(".badge-bottom-right", {
            x: 80,
            y: 40,
            z: 240,
            scale: 1.3,
            ease: "power2.out"
        }, 0.2);

        // Step 4: Hero Watermark Parallax Drift
        heroTl.to(".watermark-hero", {
            x: -100,
            opacity: 0.08,
            ease: "none"
        }, 0);
        }

        // B. Non-blocking ScrollTrigger Reveals for About and Consultation Sections
        gsap.utils.toArray("#about, .consultation-section, .transformations-section, .products-section").forEach(sec => {
            gsap.fromTo(sec, 
                { opacity: 0.3, y: 40 },
                { 
                    opacity: 1, 
                    y: 0, 
                    duration: 0.9, 
                    ease: "power2.out",
                    scrollTrigger: {
                        trigger: sec,
                        start: "top 90%",
                        toggleActions: "play none none none"
                    }
                }
            );
        });

        gsap.to(".watermark-about", {
            scrollTrigger: {
                trigger: "#about",
                start: "top bottom",
                end: "bottom top",
                scrub: 1
            },
            x: 80
        });
    }

    // ===================================================
    // ANIME.JS ENTRANCE FALLBACK
    // ===================================================
    if (hasAnime && !hasGSAP) {
        anime({
            targets: '.hero-left > *',
            translateY: [50, 0],
            opacity: [0, 1],
            delay: anime.stagger(140, { start: 200 }),
            duration: 1300,
            easing: 'easeOutQuart'
        });

        anime({
            targets: '.hero-img-card',
            rotateY: [-30, 0],
            rotateX: [15, 0],
            scale: [0.85, 1],
            opacity: [0, 1],
            delay: 400,
            duration: 1500,
            easing: 'easeOutExpo'
        });
    }

    // ===================================================
    // SCROLL-REVEAL ENGINE
    // ===================================================
    const revealObserver = new IntersectionObserver((entries) => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                const el = entry.target;
                el.classList.add('visible');

                if (hasAnime && !hasGSAP) {
                    if (el.classList.contains('reveal-left')) {
                        anime({
                            targets: el,
                            translateX: [-80, 0],
                            rotateY: [-20, 0],
                            opacity: [0, 1],
                            duration: 1100,
                            easing: 'easeOutQuart'
                        });
                    } else if (el.classList.contains('reveal-right')) {
                        anime({
                            targets: el,
                            translateX: [80, 0],
                            rotateY: [20, 0],
                            opacity: [0, 1],
                            duration: 1100,
                            easing: 'easeOutQuart'
                        });
                    } else if (el.classList.contains('reveal-scale')) {
                        anime({
                            targets: el,
                            scale: [0.88, 1],
                            rotateX: [-20, 0],
                            opacity: [0, 1],
                            duration: 900,
                            easing: 'easeOutBack(1.3)'
                        });
                    } else if (el.classList.contains('stagger-children')) {
                        Array.from(el.children).forEach(child => child.classList.add('visible'));
                        anime({
                            targets: el.children,
                            translateY: [40, 0],
                            rotateX: [-15, 0],
                            opacity: [0, 1],
                            delay: anime.stagger(80),
                            duration: 850,
                            easing: 'easeOutCubic'
                        });
                    } else {
                        anime({
                            targets: el,
                            translateY: [50, 0],
                            rotateX: [-12, 0],
                            opacity: [0, 1],
                            duration: 1000,
                            easing: 'easeOutCubic'
                        });
                    }
                }

                revealObserver.unobserve(el);
            }
        });
    }, {
        threshold: 0.05,
        rootMargin: '0px 0px 50px 0px'
    });

    document.querySelectorAll('.reveal, .reveal-left, .reveal-right, .reveal-scale, .stagger-children').forEach(el => {
        revealObserver.observe(el);
    });

    // ===================================================
    // INTERACTIVE 3D MOUSE TILT
    // ===================================================
    if (hasAnime) {
        const tiltCards = document.querySelectorAll('.hero-img-card, .consult-card, .p-card, .pc-card, .marquee-card, .about-heading img');

        tiltCards.forEach(card => {
            card.addEventListener('mousemove', (e) => {
                const rect = card.getBoundingClientRect();
                const x = e.clientX - rect.left;
                const y = e.clientY - rect.top;

                const centerX = rect.width / 2;
                const centerY = rect.height / 2;

                const rotateX = ((y - centerY) / centerY) * -12;
                const rotateY = ((x - centerX) / centerX) * 12;

                anime({
                    targets: card,
                    rotateX: rotateX,
                    rotateY: rotateY,
                    translateZ: 15,
                    duration: 400,
                    easing: 'easeOutCubic'
                });
            });

            card.addEventListener('mouseleave', () => {
                anime({
                    targets: card,
                    rotateX: 0,
                    rotateY: 0,
                    translateZ: 0,
                    duration: 600,
                    easing: 'easeOutBack(1.2)'
                });
            });
        });
    }

    // ===================================================
    // METRICS ANIMATED COUNT-UP
    // ===================================================
    const metricsStrip = document.querySelector('.metrics-strip');
    if (metricsStrip && hasAnime) {
        const metricsObserver = new IntersectionObserver((entries) => {
            if (entries[0].isIntersecting) {
                const metricItems = [
                    { el: document.querySelector('.metric:nth-child(1) h4'), targetVal: 12, suffix: '+ Yrs' },
                    { el: document.querySelector('.metric:nth-child(2) h4'), targetVal: 100, suffix: '%' },
                    { el: document.querySelector('.metric:nth-child(3) h4'), targetVal: 0, suffix: '' },
                    { el: document.querySelector('.metric:nth-child(4) h4'), targetVal: 1000, suffix: '+' }
                ];

                metricItems.forEach(item => {
                    if (item.el) {
                        const obj = { val: 0 };
                        anime({
                            targets: obj,
                            val: item.targetVal,
                            round: 1,
                            duration: 2200,
                            easing: 'easeOutExpo',
                            update: function() {
                                item.el.textContent = obj.val + item.suffix;
                            }
                        });
                    }
                });

                metricsObserver.unobserve(metricsStrip);
            }
        }, { threshold: 0.3 });

        metricsObserver.observe(metricsStrip);
    }

    // ===================================================
    // NAVBAR SCROLLED STATE
    // ===================================================
    const navbar = document.querySelector('.navbar');
    if (navbar) {
        window.addEventListener('scroll', () => {
            if (window.scrollY > 80) {
                navbar.classList.add('scrolled');
            } else {
                navbar.classList.remove('scrolled');
            }
        }, { passive: true });
    }

    // ===================================================
    // MOBILE MENU TOGGLE
    // ===================================================
    const mobileBtn = document.querySelector('.mobile-toggle');
    const drawer = document.querySelector('.mobile-drawer');

    if (mobileBtn && drawer) {
        mobileBtn.addEventListener('click', () => {
            drawer.classList.toggle('active');
            const icon = mobileBtn.querySelector('i');
            if (icon) {
                icon.classList.toggle('fa-bars');
                icon.classList.toggle('fa-xmark');
            }
        });

        drawer.querySelectorAll('a').forEach(link => {
            link.addEventListener('click', () => {
                drawer.classList.remove('active');
                const icon = mobileBtn.querySelector('i');
                if (icon) {
                    icon.classList.add('fa-bars');
                    icon.classList.remove('fa-xmark');
                }
            });
        });
    }

    // ===================================================
    // SMOOTH SCROLL WITH LENIS INTEGRATION
    // ===================================================
    document.querySelectorAll('a[href^="#"]').forEach(anchor => {
        anchor.addEventListener('click', function(e) {
            const href = this.getAttribute('href');
            if (href && href.length > 1) {
                e.preventDefault();
                const target = document.querySelector(href);
                if (target) {
                    if (lenis) {
                        const navHeight = navbar ? navbar.offsetHeight : 0;
                        lenis.scrollTo(target, { offset: -navHeight - 20, duration: 1.5 });
                    } else {
                        const navHeight = navbar ? navbar.offsetHeight : 0;
                        const top = target.getBoundingClientRect().top + window.scrollY - navHeight - 20;
                        window.scrollTo({ top, behavior: 'smooth' });
                    }
                    if (drawer) drawer.classList.remove('active');
                }
            }
        });
    });

    // ===================================================
    // CATEGORY FILTER PILLS
    // ===================================================
    const filterPills = document.querySelectorAll('.fpill');
    const catBlocks = document.querySelectorAll('.cat-block');

    filterPills.forEach(pill => {
        pill.addEventListener('click', () => {
            filterPills.forEach(p => p.classList.remove('active'));
            pill.classList.add('active');

            const filter = pill.getAttribute('data-filter');

            catBlocks.forEach(block => {
                const slug = block.getAttribute('data-category');
                if (filter === 'all' || slug === filter) {
                    block.style.display = 'block';
                    if (hasAnime) {
                        anime({
                            targets: block.querySelectorAll('.p-card, .pc-card'),
                            translateY: [40, 0],
                            rotateX: [-15, 0],
                            opacity: [0, 1],
                            scale: [0.92, 1],
                            delay: anime.stagger(70),
                            duration: 750,
                            easing: 'easeOutCubic'
                        });
                    }
                } else {
                    block.style.display = 'none';
                }
            });
        });
    });

    // ===================================================
    // LIVE PRODUCT SEARCH
    // ===================================================
    const searchInput = document.getElementById('product-search-input');
    if (searchInput) {
        searchInput.addEventListener('input', (e) => {
            const term = e.target.value.toLowerCase().trim();
            const cards = document.querySelectorAll('.p-card, .pc-card');

            cards.forEach(card => {
                const text = card.textContent.toLowerCase();
                card.style.display = text.includes(term) ? 'flex' : 'none';
            });

            catBlocks.forEach(block => {
                const visible = block.querySelectorAll('.p-card:not([style*="display: none"]), .pc-card:not([style*="display: none"])');
                block.style.display = (term && visible.length === 0) ? 'none' : 'block';
            });
        });
    }

    // ===================================================
    // TESTIMONIAL LIGHTBOX MODAL
    // ===================================================
    const lightbox = document.getElementById('lightbox-modal');
    const lbImg = document.getElementById('lightbox-img');
    const lbClose = document.getElementById('lightbox-close');

    function openLightbox(imgSrc) {
        if (imgSrc && lightbox && lbImg) {
            lbImg.src = imgSrc;
            lightbox.classList.add('active');
            document.body.style.overflow = 'hidden';

            if (hasAnime) {
                anime({
                    targets: '.lightbox-inner',
                    scale: [0.75, 1],
                    rotateX: [-15, 0],
                    opacity: [0, 1],
                    duration: 550,
                    easing: 'easeOutBack(1.5)'
                });
            }
        }
    }

    document.querySelectorAll('.t-card-click').forEach(card => {
        card.addEventListener('click', () => {
            openLightbox(card.getAttribute('data-img'));
        });
    });

    document.querySelectorAll('.t-card').forEach(card => {
        card.addEventListener('click', () => {
            const img = card.querySelector('.t-card-img img');
            if (img) openLightbox(img.src);
        });
    });

    function closeLightbox() {
        if (lightbox) {
            if (hasAnime) {
                anime({
                    targets: '.lightbox-inner',
                    scale: [1, 0.85],
                    rotateX: [0, 15],
                    opacity: [1, 0],
                    duration: 300,
                    easing: 'easeInCubic',
                    complete: function() {
                        lightbox.classList.remove('active');
                        document.body.style.overflow = '';
                    }
                });
            } else {
                lightbox.classList.remove('active');
                document.body.style.overflow = '';
            }
        }
    }

    if (lbClose) lbClose.addEventListener('click', closeLightbox);
    if (lightbox) {
        lightbox.addEventListener('click', (e) => {
            if (e.target === lightbox) closeLightbox();
        });
    }
    
    document.addEventListener('keydown', (e) => {
        if (e.key === 'Escape') closeLightbox();
    });

    // ===================================================
    // INTERACTIVE BUTTON ELASTIC HOVER
    // ===================================================
    if (hasAnime) {
        document.querySelectorAll('.btn-hero, .btn-dark-pill, .btn-nav-cta').forEach(btn => {
            btn.addEventListener('mouseenter', () => {
                anime({
                    targets: btn,
                    scale: 1.05,
                    translateZ: 10,
                    duration: 400,
                    easing: 'easeOutElastic(1, .6)'
                });
            });

            btn.addEventListener('mouseleave', () => {
                anime({
                    targets: btn,
                    scale: 1,
                    translateZ: 0,
                    duration: 400,
                    easing: 'easeOutCubic'
                });
            });
        });
    }

});
