let cachedAdminStatus;

export function fetchIsAdmin() {
  if (cachedAdminStatus !== undefined) return Promise.resolve(cachedAdminStatus);

  const baseUrl = window.location.origin;
  return fetch(`${baseUrl}/user/is_admin`)
    .then(res => res.json())
    .then(data => {
      cachedAdminStatus = data.is_admin;
      return cachedAdminStatus;
    })
    .catch(() => false);
}

