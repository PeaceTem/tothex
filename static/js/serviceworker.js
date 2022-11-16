var staticCacheName = 'neugott-lite';

const CACHE_NAME = 'offline-html';
const FALLBACK_HTML_URL = '/core/offline/'

// let this code get the cache whenever its offline
self.addEventListener('install', function(event) {
event.waitUntil(
	caches.open(staticCacheName).then(function(cache) {
	return cache.addAll([
		'/', 
		'/quiz/',
		'/question/',
		'/qxa/',
		'/leaderboard/',
		'/core/profile/',
	]);
	})
)
	caches.open(CACHE_NAME).then(function(cache){
		cache.add(new Request(FALLBACK_HTML_URL, {cache: 'reload'}))
	});
	self.skipWaiting();
});





self.addEventListener('activate',function(event){
	self.clients.claim();
});






self.addEventListener('fetch', function(event) {
var requestUrl = new URL(event.request.url);
	if (requestUrl.origin === location.origin) {
	if ((requestUrl.pathname === '/')) {
		event.respondWith(caches.match('/'));
		// window.location.href = location.origin + '/quiz/';
		return;
	}
	}
	event.respondWith(
	caches.match(event.request).then(function(response) {
		return response || fetch(event.request);
	})
	.catch(()=>{
		return caches.match(FALLBACK_HTML_URL);
	})
	);
});