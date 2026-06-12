/* coi-serviceworker — вмикає SharedArrayBuffer на GitHub Pages
 * Додає COOP + COEP заголовки через Service Worker.
 * COEP = credentialless (не блокує CDN-ресурси на відміну від require-corp)
 */

self.addEventListener("install", () => self.skipWaiting());

self.addEventListener("activate", (event) =>
  event.waitUntil(self.clients.claim())
);

self.addEventListener("fetch", function (event) {
  const request = event.request;
  if (request.method !== "GET") return;
  if (request.cache === "only-if-cached" && request.mode !== "same-origin") return;

  event.respondWith(
    fetch(request)
      .then((response) => {
        if (response.status === 0) return response;

        const newHeaders = new Headers(response.headers);
        newHeaders.set("Cross-Origin-Opener-Policy", "same-origin");
        // credentialless дозволяє CDN-ресурси (Google Fonts, jsDelivr) — на відміну від require-corp
        newHeaders.set("Cross-Origin-Embedder-Policy", "credentialless");

        return new Response(response.body, {
          status: response.status,
          statusText: response.statusText,
          headers: newHeaders,
        });
      })
      .catch(() => fetch(request))
  );
});
