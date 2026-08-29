import * as core from '@diffusionstudio/core';

// Runs INSIDE a browser (Playwright Chromium). Builds a Diffusion Studio
// composition from a JSON spec and renders it to a video Blob via core.Encoder.
// Returns { b64, type } so the Node side can write the file.
window.__render = async (spec) => {
  const w = spec.width || 1920;
  const h = spec.height || 1080;
  const comp = new core.Composition({
    width: w,
    height: h,
    background: spec.background || '#0b0e14',
  });

  for (const c of spec.clips || []) {
    const layer = await comp.add(new core.Layer());
    if (c.type === 'text') {
      const clip = new core.TextClip({
        text: c.text,
        fontSize: c.fontSize || 80,
        color: c.color || '#ffffff',
        x: c.x ?? 0,
        y: c.y ?? 0,
        width: c.width || w,
        height: c.height || h,
        start: c.start ?? 0,
        end: c.end ?? 3,
        textAlign: 'center',
        textBaseline: 'middle',
      });
      await layer.add(clip);
    } else if (c.type === 'rect') {
      const clip = new core.RectangleClip({
        fill: c.fill || '#e8482b',
        x: c.x ?? 0,
        y: c.y ?? 0,
        width: c.width || 480,
        height: c.height || 270,
        start: c.start ?? 0,
        end: c.end ?? 3,
      });
      await layer.add(clip);
    } else if (c.type === 'video') {
      const src = await core.Source.from(c.src);
      const clip = new core.VideoClip(src, {
        range: [c.start ?? 0, c.end ?? (c.start ?? 0) + 5],
      });
      await layer.add(clip);
    }
  }

  const blob = await new core.Encoder(comp).render();
  const bytes = new Uint8Array(await blob.arrayBuffer());
  let bin = '';
  const chunk = 0x8000;
  for (let i = 0; i < bytes.length; i += chunk) {
    bin += String.fromCharCode.apply(null, bytes.subarray(i, i + chunk));
  }
  return { b64: btoa(bin), type: blob.type };
};
