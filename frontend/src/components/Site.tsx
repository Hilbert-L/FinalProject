import React, { PropsWithChildren } from 'react';
import { MyProfile } from '../pages/MyProfile';
import { SearchPage } from '../pages/SearchPage';
import { Login } from '../pages/Login';
import { Register } from '../pages/Register';
import { LinkItem } from '../Types/LinkItems';
import '../styling/site.css';
import BigButton from './Buttons';
import { Route, Routes, Link, Navigate, BrowserRouter } from 'react-router-dom';
import { Layout } from '../pages/Layout';
import { ListingForm } from '../pages/ListingForm';

export const Site = (props: any) => {
  const [token, setToken] = React.useState<string | null>(null);

  React.useEffect(() => {
    const lsToken = localStorage.getItem('token');
    if (lsToken) {
      setToken(lsToken);
    }
  }, []);

  const loggedOutLinks: LinkItem[] = [
    { title: 'Search Home', path: '/' },
    { title: 'Login', path: '/login' },
    { title: 'Register', path: '/register' },
  ];

  const loggedInLinks: LinkItem[] = [
    { title: 'Home', path: '/' },
    { title: 'My Profile', path: '/myprofile' },
  ];

  const logout = async () => {
    const token = localStorage.getItem('token');
    setToken(null);
    console.log('Token is:' + token);
    localStorage.removeItem('token');
  };

  return (
    <>
      <div className="links-page">
        <h1>Parking Reservations App</h1>
        <nav>
          <div className="links-container">
            {!token &&
              loggedOutLinks.map((link: LinkItem, index: number) => (
                <div key={index} className="link-item">
                  <Link to={link.path}>
                    <span className="link-title">{link.title}</span>
                    {index !== loggedOutLinks.length - 1 && (
                      <span className="link-separator">|</span>
                    )}
                  </Link>
                </div>
              ))}
            {token &&
              loggedInLinks.map((link: LinkItem, index: number) => (
                <div key={index} className="link-item">
                  <Link to={link.path}>
                    <span className="link-title">{link.title}</span>
                    {index !== loggedInLinks.length - 1 && (
                      <span className="link-separator">|</span>
                    )}
                  </Link>
                </div>
              ))}
          </div>

          {token && (
            <>
              <BigButton onClick={logout}>
                {' '}
                <Link to="/">Logout</Link>
              </BigButton>
            </>
          )}
        </nav>
        <Routes>
          <Route
            path="/myprofile"
            element={<MyProfile setTokenFn={setToken} />}
          ></Route>
          <Route
            path="/login"
            element={<Login />}
          ></Route>
          <Route
            path="/register"
            element={<Register setTokenFn={setToken} />}
          ></Route>
          <Route
            path="/"
            element={<SearchPage setTokenFn={setToken} />}
          ></Route>
        </Routes>
      </div>
    </>
  );
}

const RequiresAuth = ({children}: PropsWithChildren) => {
    const auth = localStorage.getItem("authToken");
    const isLoggedIn = auth === "logged-in";
    // to make loggedIn true type the following into console:
    // localStorage.setItem("authToken", "logged-in")
    return isLoggedIn ? <>{children}</> : <Navigate to={"/login"} replace />
  }

function App() {
  return (
    <BrowserRouter>
      <Routes>
        <Route path="/register" element={<Register />} />
        <Route path="/login" element={<Login />} />
        <Route
          path="/"
          element={
            <RequiresAuth>
              <Layout />
            </RequiresAuth>
        } >
          <Route path="profile" element={<MyProfile />} />
          <Route path="listingform" element={<ListingForm />} />
          <Route path="" element={<SearchPage />} />
        </Route>
        <Route path="/*" element={<Navigate to="/" />} />
      </Routes>
    </BrowserRouter>
  )
}
