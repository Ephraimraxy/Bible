import { type Verse } from "@shared/schema";

export interface IStorage {
  getVerses(): Promise<Verse[]>;
}

export class MemStorage implements IStorage {
  private verses: Verse[] = [];

  constructor() {
    // Seed data for the offline Bible
    this.verses = [
      { id: 1, version: "KJV", book: "Genesis", chapter: 1, verse: 1, text: "In the beginning God created the heaven and the earth." },
      { id: 2, version: "KJV", book: "Genesis", chapter: 1, verse: 2, text: "And the earth was without form, and void; and darkness was upon the face of the deep. And the Spirit of God moved upon the face of the waters." },
      { id: 3, version: "KJV", book: "Genesis", chapter: 1, verse: 3, text: "And God said, Let there be light: and there was light." },
      { id: 4, version: "KJV", book: "John", chapter: 1, verse: 1, text: "In the beginning was the Word, and the Word was with God, and the Word was God." },
      { id: 5, version: "Hausa Bible", book: "Genesis", chapter: 1, verse: 1, text: "A fili Allah ya halicci sammai da ƙasa." },
      { id: 6, version: "Yoruba Bible", book: "Genesis", chapter: 1, verse: 1, text: "Ni atetekọṣe Ọlọrun da ọrun on aiye." },
      { id: 7, version: "Igbo Bible", book: "Genesis", chapter: 1, verse: 1, text: "Na mb͕e mbu Chineke kèrè elu-igwe na uwa." }
    ];
  }

  async getVerses(): Promise<Verse[]> {
    return this.verses;
  }
}

export const storage = new MemStorage();
