import axios from "axios";

const BASE_URL = "http://localhost:8000";  // update to Render URL when deployed

export async function sendPrompt(project, prompt) {
  const res = await axios.post(`${BASE_URL}/build`, { project, prompt });
  return res.data;
}
