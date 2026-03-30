import { NextRequest, NextResponse } from "next/server";

const GOOGLE_TTS_URL = "https://texttospeech.googleapis.com/v1/voices";

export async function GET(request: NextRequest) {
  const apiKey = process.env.GOOGLE_TTS_API_KEY;
  if (!apiKey) {
    return NextResponse.json(
      { error: "GOOGLE_TTS_API_KEY not configured" },
      { status: 503 }
    );
  }

  const language = request.nextUrl.searchParams.get("language") || "en-IN";

  try {
    const response = await fetch(
      `${GOOGLE_TTS_URL}?key=${apiKey}&languageCode=${encodeURIComponent(language)}`,
    );

    if (!response.ok) {
      return NextResponse.json(
        { error: `Google TTS API error: ${response.status}` },
        { status: response.status }
      );
    }

    const data = await response.json();
    const voices = (data.voices || []).map(
      (v: {
        name: string;
        ssmlGender: string;
        languageCodes: string[];
        naturalSampleRateHertz: number;
      }) => ({
        name: v.name,
        gender: v.ssmlGender,
        languageCodes: v.languageCodes,
        sampleRate: v.naturalSampleRateHertz,
      })
    );

    return NextResponse.json({ voices });
  } catch (error) {
    console.error("Voice list error:", error);
    return NextResponse.json(
      { error: "Failed to list voices" },
      { status: 500 }
    );
  }
}
