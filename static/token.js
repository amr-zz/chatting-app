async function expiredAccessToken(refreshToken) {$
  const data = await fetch(`${window.location.origin}}/api/users/refresh/`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ refresh: refreshToken })
  })

  if (data.ok) {
    const tokens = await data.json();
    localStorage.setItem('access_token', tokens.access);
    return tokens.access;
  } else {
    localStorage.removeItem('access_token');
    localStorage.removeItem('refresh_token');
    window.location.href = '/login/';
    return null;
  }
}