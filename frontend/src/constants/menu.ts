import { Contact, ChefHat } from "lucide-react";

interface MenuItem {
  id: string;
  label: string;
  icon: any;
  path: string;
}

export const MENU_ITEMS: MenuItem[] = [
  {
    id: "Contact",
    label: "Contact",
    icon: Contact,
    path: "/"
  },
  {
    id: "Chatbox",
    label: "Chatbox",
    icon: ChefHat,
    path: "/chatbox"
  }
];
