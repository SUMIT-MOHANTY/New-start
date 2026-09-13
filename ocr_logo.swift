import Foundation
import Vision
import AppKit

let path = "/Users/sumitmohanty/New start/New-start/media/site/WhatsApp Image 2026-09-13 at 11.46.15.jpeg"
let url = URL(fileURLWithPath: path)
guard let nsImage = NSImage(contentsOf: url),
      let cgImage = nsImage.cgImage(forProposedRect: nil, context: nil, hints: nil) else {
    print("Failed to load image")
    exit(1)
}

let request = VNRecognizeTextRequest { request, error in
    guard let observations = request.results as? [VNRecognizedTextObservation] else { return }
    for obs in observations {
        if let candidate = obs.topCandidates(1).first {
            print(candidate.string)
        }
    }
}
request.recognitionLevel = .accurate

let handler = VNImageRequestHandler(cgImage: cgImage, options: [:])
try? handler.perform([request])
