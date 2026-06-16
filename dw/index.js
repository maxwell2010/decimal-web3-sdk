import "react-native-get-random-values";
import "react-native-url-polyfill/auto";
import { Buffer } from "buffer";
import { registerRootComponent } from "expo";
import App from "./App";

global.Buffer = global.Buffer || Buffer;

registerRootComponent(App);
