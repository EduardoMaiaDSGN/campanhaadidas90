// Face boxes via Apple Vision. Usage: faces <image>... -> one line per image: "path cx cy w h" (pixels, top-left origin) or "path none"
import Foundation
import Vision
import AppKit

for path in CommandLine.arguments.dropFirst() {
    guard let img = NSImage(contentsOfFile: path),
          let cg = img.cgImage(forProposedRect: nil, context: nil, hints: nil) else {
        print("\(path) none"); continue
    }
    let W = Double(cg.width), H = Double(cg.height)
    let req = VNDetectFaceRectanglesRequest()
    try? VNImageRequestHandler(cgImage: cg, options: [:]).perform([req])
    let faces = (req.results ?? []).sorted { $0.boundingBox.width * $0.boundingBox.height > $1.boundingBox.width * $1.boundingBox.height }
    if let f = faces.first {
        let b = f.boundingBox
        let cx = (b.midX) * W, cy = (1 - b.midY) * H
        print(String(format: "%@ %.1f %.1f %.1f %.1f", path, cx, cy, b.width * W, b.height * H))
    } else {
        print("\(path) none")
    }
}
