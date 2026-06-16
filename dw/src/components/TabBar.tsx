import { ArrowLeftRight, Coins, Settings, ShieldCheck, WalletCards } from "lucide-react-native";
import { Pressable, StyleSheet, Text, View } from "react-native";
import { colors } from "@/theme";
import type { Screen } from "@/types";

const tabs: Array<{ key: Screen; label: string; Icon: typeof WalletCards }> = [
  { key: "assets", label: "Активы", Icon: WalletCards },
  { key: "swap", label: "Обмен", Icon: ArrowLeftRight },
  { key: "transfer", label: "Транзакция", Icon: Coins },
  { key: "stake", label: "Стейк", Icon: ShieldCheck },
  { key: "settings", label: "Настройки", Icon: Settings },
];

export function TabBar({ current, onChange }: { current: Screen; onChange: (screen: Screen) => void }) {
  const styles = makeStyles();
  return (
    <View style={styles.bar}>
      {tabs.map(({ key, label, Icon }) => {
        const active = current === key;
        return (
          <Pressable key={key} onPress={() => onChange(key)} style={styles.item}>
            <Icon color={active ? colors.blue : colors.dim} size={24} strokeWidth={2.2} />
            <Text style={[styles.label, active && styles.activeLabel]}>{label}</Text>
          </Pressable>
        );
      })}
    </View>
  );
}

function makeStyles() {
  return StyleSheet.create({
  activeLabel: {
    color: colors.blue,
  },
  bar: {
    alignItems: "center",
    backgroundColor: colors.tab,
    borderTopColor: colors.line,
    borderTopWidth: StyleSheet.hairlineWidth,
    flexDirection: "row",
    height: 76,
    justifyContent: "space-around",
    paddingBottom: 6,
  },
  item: {
    alignItems: "center",
    gap: 5,
    justifyContent: "center",
    minWidth: 64,
  },
  label: {
    color: colors.dim,
    fontSize: 11,
    fontWeight: "600",
  },
  });
}
