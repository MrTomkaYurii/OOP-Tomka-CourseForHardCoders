import { existsSync, readdirSync, readFileSync } from "node:fs";
import path from "node:path";
import { marked } from "marked";

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
  headings: Array<{ depth: number; text: string; slug: string }>;
};

const root = path.resolve(process.cwd(), "..");
const labsDir = path.join(root, "labs");

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
};

function slugify(value: string) {
  return value
    .toLowerCase()
    .trim()
    .replace(/[`*_[\](){}:,.!?'"|\\/]+/g, "")
    .replace(/\s+/g, "-");
}

function stripMarkdown(value: string) {
  return value
    .replace(/```[\s\S]*?```/g, " ")
    .replace(/[#>*_\-[\]()`|]/g, " ")
    .replace(/\s+/g, " ")
    .trim();
}

function collectHeadings(markdown: string) {
  return [...markdown.matchAll(/^(#{2,3})\s+(.+)$/gm)].map((match) => ({
    depth: match[1].length,
    text: match[2].trim(),
    slug: slugify(match[2]),
  }));
}

export function getLabs(): Lab[] {
  if (!existsSync(labsDir)) {
    return [];
  }

  return readdirSync(labsDir, { withFileTypes: true })
    .filter((entry) => entry.isDirectory())
    .map((entry) => entry.name)
    .filter((slug) => Boolean(meta[slug]))
    .map((slug) => {
      const sourcePath = path.join(labsDir, slug, "instructions.md");
      const markdown = readFileSync(sourcePath, "utf-8");
      const headings = collectHeadings(markdown);
      const renderer = new marked.Renderer();

      renderer.heading = ({ tokens, depth }) => {
        const text = tokens.map((token) => token.raw).join("");
        const id = slugify(text);
        return `<h${depth} id="${id}">${text}</h${depth}>`;
      };

      return {
        ...meta[slug],
        sourcePath,
        excerpt: stripMarkdown(markdown).slice(0, 180),
        headings,
        html: marked(markdown, { renderer, gfm: true }) as string,
      };
    })
    .sort((a, b) => a.number - b.number);
}

export function getLab(slug: string) {
  return getLabs().find((lab) => lab.slug === slug);
}

export const courseStats = {
  title: "OOP C# Course",
  subtitle: "Лабораторний курс, де студенти поступово будують консольну систему медичної клініки.",
  totalLabs: 21,
  domain: "Медична клініка",
  language: "C# / .NET",
};
