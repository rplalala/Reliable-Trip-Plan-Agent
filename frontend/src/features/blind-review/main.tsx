import { createRoot } from "react-dom/client";
import { BlindReview } from "./BlindReview";
import type { Presentation } from "./answers";

const data = document.getElementById("human-data");
const root = document.getElementById("root");
if (!data?.textContent || !root) throw new Error("Missing anonymous presentation data");
const presentation = JSON.parse(data.textContent) as Presentation;
createRoot(root).render(<BlindReview presentation={presentation} />);
