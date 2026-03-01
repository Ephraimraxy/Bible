import type { Express } from "express";
import type { Server } from "http";
import { storage } from "./storage";
import { api } from "@shared/routes";

export async function registerRoutes(
  httpServer: Server,
  app: Express
): Promise<Server> {
  // Sync endpoint to provide the Bible verses to the offline PWA
  app.get(api.sync.path, async (req, res) => {
    const verses = await storage.getVerses();
    res.json(verses);
  });

  return httpServer;
}
