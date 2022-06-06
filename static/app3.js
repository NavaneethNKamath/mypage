//animations
gsap.registerPlugin(ScrollTrigger)

gsap.from('.animate-hero', {
    duration: 2,
    opacity: 0,
    y: -150,
    stagger: 0.3,

});

gsap.from('.animate-services', {
    scrollTrigger: '.animate-services',
    duration: 0.7,
    opacity: 1,
    x: -150,
    stagger: 0.12,
    delay: 0.3

});

gsap.from('.animate-img', {
    scrollTrigger: '.animate-services',
    duration: 1.7,
    opacity: 0,
    x: -200,
    delay: 0.3
});



gsap.from('.animate-team', {
    scrollTrigger: '.animate-team',
    duration: 2,
    opacity: 0,
    y: -150,
    stagger: 0.3,
    delay: 0.2

});

gsap.from('.animate-janvey', {
    scrollTrigger: '.animate-janvey',
    duration: 3,
    opacity: 0,
    x: -150,
    stagger: 0.3,
    delay: 0.3

});

gsap.from('.animate-footer', {
    scrollTrigger: '.animate-footer',
    duration: 1,
    opacity: 0,
    x: -150,
    stagger: 0.3,
    delay: 0.3

});

gsap.from('.animate-email', {
    scrollTrigger: '.animate-email',
    duration: 2,
    opacity: 0,
    y: -150,
    stagger: 0.25,
    delay: 0.1

});