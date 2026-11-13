// Standalone Worker entry for the contact form endpoint.
// Re-exports only the default (Worker) handler from the shared Pages Function file,
// so the Pages-specific named exports (onRequestPost, ...) are not Worker entrypoints.
import handler from "../../functions/api/send-encrypted.js";

export default handler;
