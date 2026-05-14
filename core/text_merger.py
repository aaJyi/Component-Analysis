class TextMerger:

    def build_context_blocks(
            self,
            ocr_results,
            x_thresh=180,
            y_thresh=60):

        blocks = []

        for i, a in enumerate(ocr_results):

            try:

                ax = a['bbox'][0][0]
                ay = a['bbox'][0][1]

            except:
                continue

            neighbors = []

            for j, b in enumerate(ocr_results):

                if i == j:
                    continue

                try:

                    bx = b['bbox'][0][0]
                    by = b['bbox'][0][1]

                except:
                    continue

                if abs(ax - bx) < x_thresh and \
                        abs(ay - by) < y_thresh:

                    neighbors.append(
                        b['text']
                    )

            blocks.append({

                "text":
                    a['text'],

                "bbox":
                    a['bbox'],

                "neighbors":
                    neighbors
            })

        return blocks