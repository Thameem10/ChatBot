import { ChefHat, File } from "lucide-react";

interface MenuItem {
  id: string;
  label: string;
  icon: any;
  path: string;
}

export const MENU_ITEMS: MenuItem[] = [
  {
    id: "Upload File",
    label: "Upload File",
    icon: File,
    path: "/"
  },
  {
    id: "Chatbox",
    label: "Chatbox",
    icon: ChefHat,
    path: "/chatbox"
  }
];
