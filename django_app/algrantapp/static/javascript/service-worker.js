cacheName = 'V2'

cachedAssets = [
	'messenger.js'
	// check if saves all templates
]

self.addEventListener('install', (event) => {
	event.waitUntil(
		caches.open(cacheName)
		.then(cache => {
			console.log('Service worker: caching files...');
			cache.addAll(cachedAssets);
		})
		.catch(err => console.error(`Error while caching files: ${err}`))
	)
})

// call activation
self.addEventListener('activate', (event) => {
	console.log('Service worker activated');
	event.waitUntil(
		caches.keys()
		.then(cache_keys => {
			return Promise.all(
				cache_keys.map(this_cache => {
					if (this_cache !== cacheName) {
						console.log('Service worker: clearing old cache');
						caches.delete(cache); // remove old cache
					}
				})
			)
		})
	)
});

// call fetch
self.addEventListener('fetch', (event) => {
	console.log('Service worker: fetch event called');
	event.respondWith(
		fetch(event.request)
		.catch(() => caches.match(event.request)) // respond with the cache if there's no connection
	)
})
