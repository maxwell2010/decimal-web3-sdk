import { LinearGradient } from "expo-linear-gradient";
import { StyleSheet, Text, View } from "react-native";
import { colors, gradients, radii } from "@/theme";

export function AssetIcon({ symbol, size = 52 }: { symbol: string; size?: number }) {
  const styles = makeStyles();
  if (symbol === "DEL") {
    return (
      <LinearGradient colors={gradients.primary} start={{ x: 0, y: 0 }} end={{ x: 1, y: 1 }} style={[styles.icon, { width: size, height: size, borderRadius: size / 2 }]}>
        <Text style={[styles.del, { fontSize: size * 0.5 }]}>Ð</Text>
      </LinearGradient>
    );
  }
  return (
    <View style={[styles.gold, { width: size, height: size, borderRadius: size / 2 }]}>
      <Text style={[styles.goldText, { fontSize: size * 0.42 }]}>{symbol.slice(0, 1)}</Text>
    </View>
  );
}

function makeStyles() {
  return StyleSheet.create({
  del: {
    color: colors.white,
    fontWeight: "900",
  },
  gold: {
    alignItems: "center",
    backgroundColor: "#e2c562",
    borderColor: "#f7e7a0",
    borderWidth: 3,
    justifyContent: "center",
  },
  goldText: {
    color: "#8d7230",
    fontWeight: "900",
  },
  icon: {
    alignItems: "center",
    justifyContent: "center",
  },
  });
}
