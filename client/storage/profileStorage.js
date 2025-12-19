const PROFILE_KEY = "swiftapply_profile";

export function saveProfile(profile) {
  localStorage.setItem(PROFILE_KEY, JSON.stringify(profile));
}

export function loadProfile() {
  const data = localStorage.getItem(PROFILE_KEY);
  return data ? JSON.parse(data) : null;
}

export function clearProfile() {
  localStorage.removeItem(PROFILE_KEY);
}
