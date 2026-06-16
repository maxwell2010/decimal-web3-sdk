export const darkColors = {
  bg: "#1f2227",
  panel: "#2b2d33",
  panel2: "#303239",
  line: "#3a3d45",
  text: "#f7f8fb",
  muted: "#8f939d",
  dim: "#5d626d",
  blue: "#3d7cff",
  cyan: "#14dfb2",
  purple: "#9a38f0",
  danger: "#ff4d55",
  success: "#20d093",
  tab: "#292b31",
  black: "#15171c",
  white: "#ffffff",
};

export const lightColors = {
  bg: "#f4f7fb",
  panel: "#ffffff",
  panel2: "#eef2f7",
  line: "#d8dee8",
  text: "#151922",
  muted: "#697386",
  dim: "#9aa3b2",
  blue: "#256dff",
  cyan: "#00b894",
  purple: "#8b35ef",
  danger: "#e5484d",
  success: "#0f9f6e",
  tab: "#ffffff",
  black: "#101318",
  white: "#ffffff",
};

export let colors = darkColors;

type GradientTuple = readonly [string, string, string];

export let gradients: { primary: GradientTuple; card: GradientTuple } = {
  primary: [colors.cyan, "#38a8f5", colors.purple],
  card: ["#18d6c0", "#427ff8", "#932be8"],
};

export function setThemeMode(light: boolean) {
  colors = light ? lightColors : darkColors;
  gradients = {
    primary: [colors.cyan, "#38a8f5", colors.purple],
    card: light ? ["#12c7b0", "#3a86ff", "#8b35ef"] : ["#18d6c0", "#427ff8", "#932be8"],
  };
}

export const spacing = {
  xs: 6,
  sm: 10,
  md: 16,
  lg: 24,
  xl: 32,
};

export const radii = {
  sm: 8,
  md: 12,
  lg: 18,
  pill: 999,
};
