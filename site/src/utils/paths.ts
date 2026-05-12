const base = import.meta.env.BASE_URL;

export function sitePath(path = "/") {
  if (path === "/" || path === "") {
    return base;
  }

  const normalizedBase = base.endsWith("/") ? base.slice(0, -1) : base;
  const normalizedPath = path.startsWith("/") ? path : `/${path}`;

  return `${normalizedBase}${normalizedPath}`;
}

export function pathWithoutBase(pathname: string) {
  if (base === "/" || !pathname.startsWith(base)) {
    return pathname;
  }

  const withoutBase = pathname.slice(base.length);
  return `/${withoutBase}`.replace(/\/+/g, "/");
}
