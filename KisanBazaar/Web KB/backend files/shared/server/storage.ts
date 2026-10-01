import { type User, type InsertUser, type Product, type InsertProduct, type Order, type InsertOrder } from "@shared/schema";
import { randomUUID } from "crypto";
import fs from "fs";
import path from "path";

export class MemStorage implements IStorage {
  private users: Map<string, User>;
  private products: Map<string, Product>;
  private orders: Map<string, Order>;

  constructor() {
    this.users = new Map();
    this.products = new Map();
    this.orders = new Map();
    this.loadProductsFromJSON();
  }

  private async loadProductsFromJSON() {
    try {
      const productsPath = path.resolve(process.cwd(), "attached_assets/products_1753770661172.json");
      const productsData = JSON.parse(fs.readFileSync(productsPath, "utf-8"));
      
      for (const [category, items] of Object.entries(productsData)) {
        for (const item of items as any[]) {
          const product: Product = {
            id: randomUUID(),
            name: item.name,
            price: item.price.toString(),
            quantity: item.quantity || item.quantitykg || 0,
            unit: item.unit || "piece",
            category: category,
            image: item.image,
            description: `Fresh ${item.name.toLowerCase()} from local farmers`,
            createdAt: new Date(),
          };
          this.products.set(product.id, product);
        }
      }
    } catch (error) {
      console.error("Failed to load products from JSON:", error);
    }
  }

  // CRUD operations for products, orders, users
}