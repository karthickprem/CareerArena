import { NextRequest, NextResponse } from "next/server";

const GOOGLE_TTS_URL = "https://texttospeech.googleapis.com/v1/text:synthesize";

export async function POST(request: NextRequest) {
  const apiKey = process.env.GOOGLE_TTS_API_KEY;
  if (!apiKey) {
    return NextResponse.json(
      { error: "TTS not configured — add GOOGLE_TTS_API_KEY to .env.local" },
      { status: 503 }
    );
  }

  try {
    const { text, googleVoiceName, languageCode, speakingRate, pitch } =
      await request.json();

    if (!text || !googleVoiceName) {
      return NextResponse.json(
        { error: "text and googleVoiceName are required" },
        { status: 400 }
      );
    }

    const response = await fetch(`${GOOGLE_TTS_URL}?key=${apiKey}`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({
        input: { text },
        voice: {
          languageCode: languageCode || "en-IN",
          name: googleVoiceName,
        },
        audioConfig: {
          audioEncoding: "MP3",
          speakingRate: speakingRate ?? 1.0,
          pitch: pitch ?? 0.0,
          sampleRateHertz: 24000,
        },
      }),
    });

    if (!response.ok) {
      const errorText = await response.text().catch(() => "Unknown error");
      console.error(`Google TTS error (${response.status}): ${errorText}`);
      return NextResponse.json(
        { error: `Google TTS API error: ${response.status}` },
        { status: response.status }
      );
    }

    const data = await response.json();
    const audioBytes = Buffer.from(data.audioContent, "base64");

    return new NextResponse(audioBytes, {
      status: 200,
      headers: {
        "Content-Type": "audio/mpeg",
        "Cache-Control": "public, max-age=3600",
      },
    });
  } catch (error) {
    console.error("TTS route error:", error);
    return NextResponse.json(
      { error: "Failed to generate speech" },
      { status: 500 }
    );
  }
}
