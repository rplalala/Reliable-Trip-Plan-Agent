import { type RouteObject, createBrowserRouter } from "react-router-dom";

import { DeveloperLayout } from "../layouts/DeveloperLayout";
import { ProductLayout } from "../layouts/ProductLayout";
import { DeveloperPlannerPage } from "../routes/developer/DeveloperPlannerPage";
import { NotFoundPage } from "../routes/NotFoundPage";
import { HomePage } from "../routes/product/HomePage";
import { PlanTripPage } from "../routes/product/PlanTripPage";

export const routes: RouteObject[] = [
  {
    element: <ProductLayout />,
    children: [
      { index: true, element: <HomePage /> },
      { path: "plan", element: <PlanTripPage /> },
    ],
  },
  {
    path: "dev",
    element: <DeveloperLayout />,
    children: [
      { index: true, element: <DeveloperPlannerPage /> },
    ],
  },
  { path: "*", element: <NotFoundPage /> },
];

export const router = createBrowserRouter(routes);
