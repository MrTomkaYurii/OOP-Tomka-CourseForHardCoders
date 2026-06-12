/* coi-serviceworker — вмикає SharedArrayBuffer на GitHub Pages
 * Додає Cross-Origin-Opener-Policy та Cross-Origin-Embedder-Policy заголовки
 * через Service Worker, щоб WASM threading (System.Threading.Thread) працював.
 */

self.addEventListener("install", () => self.skipWaiting());

self.addEventListener("activate", (event) =>
  event.waitUntil(self.clients.claim())
);

self.addEventListener("fetch", function (event) {
  const request = event.request;

  // Пропускаємо non-GET запити і cross-origin only-if-cached
  if (request.method !== "GET") return;
  if (request.cache === "only-if-cached" && request.mode !== "same-origin") return;

  event.respondWith(
    fetch(request)
      .then((response) => {
        // Не чіпаємо opaque responses (status 0)
        if (response.status === 0) return response;

        const newHeaders = new Headers(response.headers);
        newHeaders.set("Cross-Origin-Opener-Policy", "same-origin");
        newHeaders.set("Cross-Origin-Embedder-Policy", "require-corp");

        return new Response(response.body, {
          status: response.status,
          statusText: response.statusText,
          headers: newHeaders,
        });
      })
      .catch((e) => {
        console.warn("[coi-serviceworker] fetch error:", e);
        return fetch(request);
      })
  );
});
