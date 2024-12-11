console.log('main js file called');

window.addEventListener('load', (event) => {
    // call service worker
    if (navigator.serviceWorker) {
        console.log('Service worker can be registered. Calling service worker...');
        navigator.serviceWorker
        .register('service-worker.js', {scope: '/'})
        .then(console.log('Service worker registered'))
        .catch(err => console.error(`Erroro during service worker's registration: ${err}`))
    }
})