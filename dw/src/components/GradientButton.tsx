import { LinearGradient } from "expo-linear-gradient";
import { Pressable, StyleSheet, Text, ViewStyle } from "react-native";
import { colors, gradients, radii } from "@/theme";

export function GradientButton({
  title,
  disabled,
  onPress,
  style,
}: {
  title: string;
  disabled?: boolean;
  onPress?: () => void;
  style?: ViewStyle;
}) {
  const styles = makeStyles();
  if (disabled) {
    return (
      <Pressable disabled style={[styles.disabled, style]}>
        <Text style={styles.disabledText}>{title}</Text>
      </Pressable>
    );
  }
  return (
    <Pressable onPress={onPress} style={style}>
      <LinearGradient colors={gradients.primary} start={{ x: 0, y: 0.5 }} end={{ x: 1, y: 0.5 }} style={styles.button}>
        <Text style={styles.text}>{title}</Text>
      </LinearGradient>
    </Pressable>
  );
}

function makeStyles() {
  return StyleSheet.create({
  button: {
    alignItems: "center",
    borderRadius: radii.md,
    height: 64,
    justifyContent: "center",
  },
  disabled: {
    alignItems: "center",
    backgroundColor: colors.panel,
    borderRadius: radii.md,
    height: 64,
    justifyContent: "center",
  },
  disabledText: {
    color: colors.dim,
    fontSize: 20,
    fontWeight: "800",
  },
  text: {
    color: colors.white,
    fontSize: 20,
    fontWeight: "800",
  },
  });
}
