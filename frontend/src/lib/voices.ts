/**
 * Voice configuration for CareerArena panel interviewers.
 *
 * Primary: Google Cloud TTS with Indian English (en-IN) voices.
 * Fallback: Web Speech API (browser-native, free, zero cost).
 *
 * Google Cloud TTS voice tiers (quality ascending):
 *   Standard < Wavenet < Neural2 < Journey
 * We use Wavenet as the default — good quality, reasonable cost.
 *
 * Pricing (as of 2026):
 *   Wavenet:  $16 / 1M characters  (~₹0.02 per interview session)
 *   Neural2:  $16 / 1M characters
 *   Standard: $4  / 1M characters
 */

export interface VoiceConfig {
  googleVoiceName: string;
  languageCode: string;
  speakingRate: number;
  pitch: number;

  webSpeechLang: string;
  webSpeechRate: number;
  webSpeechPitch: number;
}

const VOICE_MAP: Record<string, VoiceConfig> = {
  // Female voices — HR / VP / friendly personas
  "Priya Sharma": {
    googleVoiceName: "en-IN-Wavenet-A",
    languageCode: "en-IN",
    speakingRate: 0.95,
    pitch: 1.0,
    webSpeechLang: "en-IN",
    webSpeechRate: 0.95,
    webSpeechPitch: 1.1,
  },
  "Meera Krishnan": {
    googleVoiceName: "en-IN-Wavenet-D",
    languageCode: "en-IN",
    speakingRate: 0.9,
    pitch: -1.0,
    webSpeechLang: "en-IN",
    webSpeechRate: 0.9,
    webSpeechPitch: 0.9,
  },

  // Male voices — Tech / Domain / challenging personas
  "Arjun Mehta": {
    googleVoiceName: "en-IN-Wavenet-B",
    languageCode: "en-IN",
    speakingRate: 1.0,
    pitch: 0.0,
    webSpeechLang: "en-IN",
    webSpeechRate: 1.0,
    webSpeechPitch: 1.0,
  },
  "Vikram Desai": {
    googleVoiceName: "en-IN-Wavenet-C",
    languageCode: "en-IN",
    speakingRate: 0.95,
    pitch: -2.0,
    webSpeechLang: "en-IN",
    webSpeechRate: 0.95,
    webSpeechPitch: 0.8,
  },
  "Ravi Anand": {
    googleVoiceName: "en-IN-Neural2-B",
    languageCode: "en-IN",
    speakingRate: 1.05,
    pitch: 1.0,
    webSpeechLang: "en-IN",
    webSpeechRate: 1.05,
    webSpeechPitch: 1.0,
  },

  // UPSC personas — more formal, slightly slower
  "Justice K. Ramaswamy": {
    googleVoiceName: "en-IN-Wavenet-C",
    languageCode: "en-IN",
    speakingRate: 0.85,
    pitch: -3.0,
    webSpeechLang: "en-IN",
    webSpeechRate: 0.85,
    webSpeechPitch: 0.7,
  },
  "Prof. Sunita Narayan": {
    googleVoiceName: "en-IN-Neural2-A",
    languageCode: "en-IN",
    speakingRate: 0.9,
    pitch: 2.0,
    webSpeechLang: "en-IN",
    webSpeechRate: 0.9,
    webSpeechPitch: 1.2,
  },
  "Cmdr. Rajesh Verma": {
    googleVoiceName: "en-IN-Neural2-C",
    languageCode: "en-IN",
    speakingRate: 1.0,
    pitch: -1.0,
    webSpeechLang: "en-IN",
    webSpeechRate: 1.0,
    webSpeechPitch: 0.9,
  },
};

const FALLBACK_MALE: VoiceConfig = {
  googleVoiceName: "en-IN-Wavenet-B",
  languageCode: "en-IN",
  speakingRate: 1.0,
  pitch: 0.0,
  webSpeechLang: "en-IN",
  webSpeechRate: 1.0,
  webSpeechPitch: 1.0,
};

const FALLBACK_FEMALE: VoiceConfig = {
  googleVoiceName: "en-IN-Wavenet-A",
  languageCode: "en-IN",
  speakingRate: 0.95,
  pitch: 0.0,
  webSpeechLang: "en-IN",
  webSpeechRate: 0.95,
  webSpeechPitch: 1.1,
};

const FEMALE_NAMES = new Set([
  "priya", "meera", "sunita", "anita", "sneha", "kavita",
  "deepa", "lakshmi", "sita", "radha", "nandini", "pooja",
]);

export function getVoiceConfig(speakerName: string): VoiceConfig {
  if (VOICE_MAP[speakerName]) {
    return VOICE_MAP[speakerName];
  }

  const firstName = speakerName.split(" ")[0].toLowerCase();
  if (FEMALE_NAMES.has(firstName)) {
    return FALLBACK_FEMALE;
  }
  return FALLBACK_MALE;
}

export function setVoiceConfig(speakerName: string, config: VoiceConfig) {
  VOICE_MAP[speakerName] = config;
}
