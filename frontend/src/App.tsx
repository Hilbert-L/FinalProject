import { BrowserRouter, Route, Routes } from "react-router-dom";
import { SearchPage } from "./pages/SearchPage";
import { MyProfile } from "./pages/MyProfile";
import { Layout } from "./pages/Layout";

function App() {
  return (
    <BrowserRouter>
      <Routes>
        <Route path="/" element={<Layout />} >
          <Route path="search" element={<SearchPage />} />
          <Route path="profile" element={<MyProfile />} />
        </Route>
      </Routes>
    </BrowserRouter>
  )
}

export default App
