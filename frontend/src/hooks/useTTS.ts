"use client";

import { useState, useRef, useCallback, useEffect } from "react";
import { getVoiceConfig } from "@/lib/voices";

interface UseTTSOptions {
  onStart?: () => void;
  onEnd?: () => void;
}

interface UseTTSReturn {
  speak: (text: string, speakerName: string, onComplete?: () => void) => Promise<void>;
  stop: () => void;
  isSpeaking: boolean;
  isMuted: boolean;
  toggleMute: () => void;
  isAvailable: boolean;
  provider: "google" | "browser" | "none";
}

/**
 * TTS hook with two providers:
 *   1. Google Cloud TTS (server-side, Indian English voices) — requires GOOGLE_TTS_API_KEY
 *   2. Web Speech API (browser-native, free fallback)
 */
export function useTTS(options?: UseTTSOptions): UseTTSReturn {
  const [isSpeaking, setIsSpeaking] = useState(false);
  const [isMuted, setIsMuted] = useState(false);
  const [provider, setProvider] = useState<"google" | "browser" | "none">("google");
  const audioRef = useRef<HTMLAudioElement | null>(null);
  const abortRef = useRef<AbortController | null>(null);
  const onCompleteRef = useRef<(() => void) | null>(null);

  const isAvailable = provider !== "none";

  useEffect(() => {
    audioRef.current = new Audio();
    audioRef.current.addEventListener("ended", () => {
      setIsSpeaking(false);
      options?.onEnd?.();
      onCompleteRef.current?.();
      onCompleteRef.current = null;
    });
    audioRef.current.addEventListener("error", () => {
      setIsSpeaking(false);
      options?.onEnd?.();
      onCompleteRef.current?.();
      onCompleteRef.current = null;
    });

    return () => {
      if (audioRef.current) {
        audioRef.current.pause();
        audioRef.current.removeAttribute("src");
      }
      window.speechSynthesis?.cancel();
    };
  }, []);

  const speakWithBrowser = useCallback(
    (text: string, speakerName: string) => {
      const synth = window.speechSynthesis;
      if (!synth) {
        options?.onEnd?.();
        return;
      }

      synth.cancel();
      const voiceConfig = getVoiceConfig(speakerName);
      const utterance = new SpeechSynthesisUtterance(text);
      utterance.lang = voiceConfig.webSpeechLang;
      utterance.rate = voiceConfig.webSpeechRate;
      utterance.pitch = voiceConfig.webSpeechPitch;

      const voices = synth.getVoices();
      const indianVoice = voices.find(
        (v) => v.lang === "en-IN" || v.lang.startsWith("en-IN")
      );
      if (indianVoice) {
        utterance.voice = indianVoice;
      }

      utterance.onend = () => {
        setIsSpeaking(false);
        options?.onEnd?.();
        onCompleteRef.current?.();
        onCompleteRef.current = null;
      };
      utterance.onerror = () => {
        setIsSpeaking(false);
        options?.onEnd?.();
        onCompleteRef.current?.();
        onCompleteRef.current = null;
      };

      setIsSpeaking(true);
      options?.onStart?.();
      synth.speak(utterance);
    },
    [options]
  );

  const speak = useCallback(
    async (text: string, speakerName: string, onComplete?: () => void) => {
      onCompleteRef.current = onComplete || null;

      if (isMuted || !text.trim()) {
        options?.onEnd?.();
        onComplete?.();
        onCompleteRef.current = null;
        return;
      }

      if (audioRef.current) {
        audioRef.current.pause();
      }
      window.speechSynthesis?.cancel();
      if (abortRef.current) {
        abortRef.current.abort();
      }

      // Browser fallback — skip server call
      if (provider === "browser") {
        speakWithBrowser(text, speakerName);
        return;
      }

      const voiceConfig = getVoiceConfig(speakerName);
      abortRef.current = new AbortController();

      try {
        setIsSpeaking(true);
        options?.onStart?.();

        const response = await fetch("/api/tts", {
          method: "POST",
          headers: { "Content-Type": "application/json" },
          body: JSON.stringify({
            text,
            googleVoiceName: voiceConfig.googleVoiceName,
            languageCode: voiceConfig.languageCode,
            speakingRate: voiceConfig.speakingRate,
            pitch: voiceConfig.pitch,
          }),
          signal: abortRef.current.signal,
        });

        if (!response.ok) {
          if (response.status === 503) {
            // Google TTS not configured — fall back to Web Speech API
            const hasBrowserTTS = typeof window !== "undefined" && "speechSynthesis" in window;
            setProvider(hasBrowserTTS ? "browser" : "none");
            if (hasBrowserTTS) {
              speakWithBrowser(text, speakerName);
              return;
            }
          }
          setIsSpeaking(false);
          options?.onEnd?.();
          onCompleteRef.current?.();
          onCompleteRef.current = null;
          return;
        }

        const audioBlob = await response.blob();
        const audioUrl = URL.createObjectURL(audioBlob);

        if (audioRef.current) {
          audioRef.current.src = audioUrl;
          await audioRef.current.play();
        }
      } catch (error) {
        if ((error as Error).name !== "AbortError") {
          console.error("TTS speak error:", error);
        }
        setIsSpeaking(false);
        options?.onEnd?.();
        onCompleteRef.current?.();
        onCompleteRef.current = null;
      }
    },
    [isMuted, options, provider, speakWithBrowser]
  );

  const stop = useCallback(() => {
    if (abortRef.current) {
      abortRef.current.abort();
    }
    if (audioRef.current) {
      audioRef.current.pause();
      audioRef.current.currentTime = 0;
    }
    window.speechSynthesis?.cancel();
    onCompleteRef.current = null;
    setIsSpeaking(false);
  }, []);

  const toggleMute = useCallback(() => {
    setIsMuted((prev) => {
      if (!prev) {
        if (audioRef.current) {
          audioRef.current.pause();
        }
        window.speechSynthesis?.cancel();
        setIsSpeaking(false);
        onCompleteRef.current?.();
        onCompleteRef.current = null;
      }
      return !prev;
    });
  }, []);

  return { speak, stop, isSpeaking, isMuted, toggleMute, isAvailable, provider };
}
