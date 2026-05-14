import { existsSync, readdirSync, readFileSync } from "node:fs";
import path from "node:path";
import { marked } from "marked";
import { getSingletonHighlighter } from "shiki";

export type LabStatus = "ready" | "draft" | "planned";

export type Lab = {
  slug: string;
  number: number;
  title: string;
  topic: string;
  status: LabStatus;
  module: string;
  branch: string;
  merge: string;
  menu: string;
  difficulty: 1 | 2 | 3;
  sourcePath: string;
  excerpt: string;
  html: string;
  headings: Array<Heading>;
};

export type Heading = { depth: number; text: string; slug: string };

export type Lecture = {
  slug: string;
  number: number;
  numberLabel: string;
  title: string;
  chapter: number;
  chapterTitle: string;
  section: number;
  sections: Array<{ text: string; slug: string }>;
  sourcePath: string;
  excerpt: string;
  html: string;
  headings: Array<Heading>;
};

const root = path.resolve(process.cwd(), "..");
const labsDir = path.join(root, "labs");
const lecturesDir = path.join(root, "lectures");
const lectureSectionsDir = path.join(lecturesDir, "sections");
const lectureSummariesPath = path.join(lectureSectionsDir, "summaries.json");
const base = import.meta.env.BASE_URL;

function siteAssetPath(assetPath: string) {
  const normalizedBase = base.endsWith("/") ? base.slice(0, -1) : base;
  const normalizedPath = assetPath.startsWith("/") ? assetPath : `/${assetPath}`;

  return `${normalizedBase}${normalizedPath}`;
}

function lectureChapterTitle(chapter: number, fallback = `Розділ ${chapter}`) {
  if (chapter === 1) {
    return "Розділ 1. Вступ";
  }

  if (chapter === 2) {
    return "Розділ 2. Основи програмування на C#";
  }

  if (chapter === 3) {
    return "Розділ 3. Класи, структури та простір імен";
  }

  return fallback;
}

const meta: Record<string, Omit<Lab, "sourcePath" | "excerpt" | "html" | "headings">> = {
  "lab-01-intro": {
    slug: "lab-01-intro",
    number: 1,
    title: "Основи C#",
    topic: "Типи, умови, цикли, методи",
    status: "ready",
    module: "Sandbox",
    branch: "sandbox/intro",
    merge: "не зливається",
    menu: "окремий консольний проєкт",
    difficulty: 1,
  },
  "lab-02-arrays": {
    slug: "lab-02-arrays",
    number: 2,
    title: "Масиви",
    topic: "Пошук, сортування, 2D-розклад",
    status: "ready",
    module: "Sandbox",
    branch: "sandbox/arrays",
    merge: "не зливається",
    menu: "окремий консольний проєкт",
    difficulty: 1,
  },
  "lab-03-classes": {
    slug: "lab-03-classes",
    number: 3,
    title: "Класи",
    topic: "Patient, Doctor, Appointment",
    status: "ready",
    module: "Catalog",
    branch: "feature/catalog",
    merge: "main",
    menu: "Пацієнти, лікарі, записи, звіт",
    difficulty: 2,
  },
  "lab-04-class-members": {
    slug: "lab-04-class-members",
    number: 4,
    title: "Члени класу",
    topic: "enum, struct, static, overload",
    status: "ready",
    module: "Core types",
    branch: "feature/class-members",
    merge: "main",
    menu: "типи крові, спеціальності, статистика",
    difficulty: 2,
  },
  "lab-05-encapsulation": {
    slug: "lab-05-encapsulation",
    number: 5,
    title: "Інкапсуляція",
    topic: "private fields, validation, try/catch",
    status: "ready",
    module: "Patients+",
    branch: "feature/encapsulation",
    merge: "main",
    menu: "зрозумілі помилки замість падіння",
    difficulty: 3,
  },
  "lab-06-inheritance": {
    slug: "lab-06-inheritance",
    number: 6,
    title: "Наслідування",
    topic: "MedicalRecord, Diagnosis, LabResult",
    status: "ready",
    module: "Medical records",
    branch: "feature/inheritance",
    merge: "main",
    menu: "медична картка",
    difficulty: 3,
  },
  "lab-07-interfaces": {
    slug: "lab-07-interfaces",
    number: 7,
    title: "Інтерфейси",
    topic: "IPayable, ICancellable, ISchedulable",
    status: "ready",
    module: "Billing",
    branch: "feature/interfaces",
    merge: "main",
    menu: "рахунки",
    difficulty: 3,
  },
  "lab-08-polymorphism": {
    slug: "lab-08-polymorphism",
    number: 8,
    title: "Поліморфізм",
    topic: "override, sealed, runtime dispatch",
    status: "ready",
    module: "Appointments+",
    branch: "feature/polymorphism",
    merge: "разом з Lab 09",
    menu: "внутрішні типи прийомів",
    difficulty: 3,
  },
  "lab-09-generics": {
    slug: "lab-09-generics",
    number: 9,
    title: "Generics",
    topic: "List<T>, Queue<T>, constraints",
    status: "ready",
    module: "Waiting",
    branch: "feature/generics",
    merge: "main",
    menu: "черга очікування",
    difficulty: 3,
  },
  "lab-10-iterators": {
    slug: "lab-10-iterators",
    number: 10,
    title: "Ітератори та компаратори",
    topic: "IComparable, IComparer, analytics",
    status: "ready",
    module: "Analytics",
    branch: "feature/iterators",
    merge: "main",
    menu: "аналітика",
    difficulty: 3,
  },
  "lab-11-reflection": {
    slug: "lab-11-reflection",
    number: 11,
    title: "Reflection & Attributes",
    topic: "атрибути, рефлексія, валідатор",
    status: "ready",
    module: "Treatment plans",
    branch: "feature/reflection",
    merge: "main",
    menu: "плани лікування, автогенерація форм",
    difficulty: 3,
  },
  "lab-12-files": {
    slug: "lab-12-files",
    number: 12,
    title: "File I/O",
    topic: "логування, CSV, збереження стану",
    status: "ready",
    module: "Persistence",
    branch: "feature/files",
    merge: "main",
    menu: "журнал, імпорт, експорт, сесія",
    difficulty: 3,
  },
  "lab-13-events": {
    slug: "lab-13-events",
    number: 13,
    title: "Events & Delegates",
    topic: "EventArgs, event, обробники",
    status: "ready",
    module: "Automation",
    branch: "feature/events",
    merge: "main",
    menu: "автоматичні реакції системи",
    difficulty: 3,
  },
};

function slugify(value: string) {
  return value
    .toLowerCase()
    .trim()
    .replace(/[`*_[\](){}:,.!?'"|\\/]+/g, "")
    .replace(/\s+/g, "-");
}

function uniqueSlug(baseSlug: string, counts: Map<string, number>) {
  const nextCount = (counts.get(baseSlug) ?? 0) + 1;
  counts.set(baseSlug, nextCount);
  return nextCount === 1 ? baseSlug : `${baseSlug}-${nextCount}`;
}

function stripMarkdown(value: string) {
  return value
    .replace(/```[\s\S]*?```/g, " ")
    .replace(/[#>*_\-[\]()`|]/g, " ")
    .replace(/\s+/g, " ")
    .trim();
}

function parseFrontmatter(markdown: string) {
  const match = markdown.match(/^\uFEFF?---\r?\n([\s\S]*?)\r?\n---\r?\n?/);

  if (!match) {
    return { data: {} as Record<string, string>, body: markdown };
  }

  const raw = match[1].trim();
  const body = markdown.slice(match[0].length).replace(/^\s+/, "");
  const data: Record<string, string> = {};

  for (const line of raw.split("\n")) {
    const separator = line.indexOf(":");
    if (separator === -1) {
      continue;
    }

    const key = line.slice(0, separator).trim();
    const value = line.slice(separator + 1).trim().replace(/^"|"$/g, "");
    data[key] = value;
  }

  return { data, body };
}

function getLectureSummaries() {
  if (!existsSync(lectureSummariesPath)) {
    return {} as Record<string, string>;
  }

  return JSON.parse(readFileSync(lectureSummariesPath, "utf-8")) as Record<string, string>;
}

// ── Shiki singleton ────────────────────────────────────────────────────────
async function getHighlighter() {
  return getSingletonHighlighter({
    themes: ["github-dark"],
    langs: ["csharp", "typescript", "javascript", "json", "bash", "text", "markdown", "xml", "sql"],
  });
}

function collectHeadings(markdown: string, minDepth = 2) {
  const counts = new Map<string, number>();

  return [...markdown.matchAll(/^(#{1,3})\s+(.+)$/gm)]
    .filter((match) => match[1].length >= minDepth)
    .map((match) => ({
    depth: match[1].length,
    text: match[2].trim(),
    slug: uniqueSlug(slugify(match[2]), counts),
  }));
}

async function renderMarkdown(markdown: string, options: { assetPrefix?: string } = {}) {
  const highlighter = await getHighlighter();
  const supportedLangs = highlighter.getLoadedLanguages();

  const renderHeadings = collectHeadings(markdown, 1);
  const headings = renderHeadings.filter((heading) => heading.depth >= 2);
  const renderer = new marked.Renderer();
  let headingIndex = 0;

  renderer.heading = ({ tokens, depth }) => {
    const text = tokens.map((token) => token.raw).join("");
    const id = depth <= 3 ? renderHeadings[headingIndex]?.slug ?? slugify(text) : slugify(text);

    if (depth <= 3) {
      headingIndex += 1;
    }

    return `<h${depth} id="${id}">${text}</h${depth}>`;
  };

  renderer.code = ({ text, lang }) => {
    const language = lang && supportedLangs.includes(lang as any) ? (lang as any) : "text";
    return highlighter.codeToHtml(text, { lang: language, theme: "github-dark" });
  };

  const preparedMarkdown = options.assetPrefix
    ? markdown.replace(/\]\(assets\/docx\/([^)]+)\)/g, `](${options.assetPrefix}/$1)`)
    : markdown;

  return {
    headings,
    allHeadings: renderHeadings,
    html: await marked(preparedMarkdown, { renderer, gfm: true }) as string,
  };
}

// ── Build-time cache (computed once per build) ─────────────────────────────
let _labsCache: Promise<Lab[]> | null = null;
let _lecturesCache: Promise<Lecture[]> | null = null;

export function getLabs(): Promise<Lab[]> {
  if (_labsCache) return _labsCache;

  _labsCache = (async () => {
    if (!existsSync(labsDir)) return [];

    const slugs = readdirSync(labsDir, { withFileTypes: true })
      .filter((entry) => entry.isDirectory())
      .map((entry) => entry.name)
      .filter((slug) => Boolean(meta[slug]));

    const labs = await Promise.all(
      slugs.map(async (slug) => {
        const sourcePath = path.join(labsDir, slug, "instructions.md");
        const markdown = readFileSync(sourcePath, "utf-8");
        const rendered = await renderMarkdown(markdown);

        return {
          ...meta[slug],
          sourcePath,
          excerpt: stripMarkdown(markdown).slice(0, 180),
          headings: rendered.headings,
          html: rendered.html,
        };
      }),
    );

    return labs.sort((a, b) => a.number - b.number);
  })();

  return _labsCache;
}

export async function getLab(slug: string) {
  return (await getLabs()).find((lab) => lab.slug === slug);
}

export function getLectures(): Promise<Lecture[]> {
  if (_lecturesCache) return _lecturesCache;

  _lecturesCache = (async () => {
    if (!existsSync(lectureSectionsDir)) return [];

    const summaries = getLectureSummaries();

    const entries = readdirSync(lectureSectionsDir, { withFileTypes: true })
      .filter((entry) => entry.isFile() && /^\d{2}-.+\.md$/.test(entry.name))
      .sort((a, b) => a.name.localeCompare(b.name));

    const lectures = await Promise.all(
      entries.map(async (entry) => {
        const sourcePath = path.join(lectureSectionsDir, entry.name);
        const rawMarkdown = readFileSync(sourcePath, "utf-8");
        const { data, body: markdown } = parseFrontmatter(rawMarkdown);
        const chapter = Number(data.chapter ?? entry.name.slice(0, 2));
        const section = Number(data.section ?? entry.name.slice(3, 5));
        const numberLabel = data.number ?? `${chapter}.${section}`;
        const slug = entry.name.replace(/\.md$/, "");
        const title = data.title ?? markdown.match(/^##\s+(.+)$/m)?.[1]?.trim() ?? `Лекція ${numberLabel}`;
        const chapterTitle = data.chapterTitle ?? lectureChapterTitle(chapter);
        const rendered = await renderMarkdown(markdown, { assetPrefix: siteAssetPath("/lecture-assets/docx") });
        const summary = summaries[slug];

        return {
          slug,
          number: chapter * 100 + section,
          title,
          chapter,
          chapterTitle,
          sections: [],
          section,
          numberLabel,
          sourcePath,
          excerpt: summary ?? stripMarkdown(markdown).slice(0, 210),
          headings: rendered.headings,
          html: rendered.html,
        };
      }),
    );

    return lectures.sort((a, b) => a.chapter - b.chapter || Number(a.numberLabel.split(".")[1]) - Number(b.numberLabel.split(".")[1]));
  })();

  return _lecturesCache;
}

export async function getLecture(slug: string) {
  return (await getLectures()).find((lecture) => lecture.slug === slug);
}

export const courseStats = {
  title: "OOP C# Course",
  subtitle: "Лабораторний курс, де студенти поступово будують консольну систему медичної клініки.",
  totalLabs: 21,
  domain: "Медична клініка",
  language: "C# / .NET",
};
