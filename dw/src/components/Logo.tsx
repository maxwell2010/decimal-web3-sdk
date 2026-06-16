import { Image, StyleSheet } from "react-native";

export function Logo({ size = 58 }: { size?: number }) {
  return (
    <Image
      source={require("../../assets/candywallet-logo-ui.png")}
      resizeMode="contain"
      style={[styles.logo, { width: size * 1.55, height: size * 1.55 }]}
    />
  );
}

const styles = StyleSheet.create({
  logo: {
    alignSelf: "flex-start",
  },
});
