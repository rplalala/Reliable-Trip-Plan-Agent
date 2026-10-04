import { defineConfig } from "vite";

export default defineConfig({
  define: { "process.env.NODE_ENV": JSON.stringify("production") },
  build: {
    outDir: "dist-blind-review",
    sourcemap: false,
    cssCodeSplit: false,
    lib: { entry: "src/features/blind-review/main.tsx", name: "BlindReview", formats: ["iife"], fileName: () => "review.js", cssFileName: "review" },
  },
});
