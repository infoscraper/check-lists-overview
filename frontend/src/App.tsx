import { BrowserRouter as Router, Routes, Route, Link, useLocation } from 'react-router-dom';
import Dashboard from './components/Dashboard';
import TableView from './components/TableView';
import './App.css';

function NavLinks() {
  const location = useLocation();
  
  return (
    <div className="nav-links">
      <Link 
        to="/" 
        className={`nav-link ${location.pathname === '/' ? 'active' : ''}`}
      >
        <span className="nav-link-ru">Обзор</span>
        <span className="nav-link-en">Overview</span>
      </Link>
      <Link 
        to="/details" 
        className={`nav-link ${location.pathname === '/details' ? 'active' : ''}`}
      >
        <span className="nav-link-ru">Детализация чек-листов</span>
        <span className="nav-link-en">Controls</span>
      </Link>
    </div>
  );
}

function App() {
  return (
    <Router>
      <div className="app">
        <nav className="navbar">
          <div className="nav-container">
            <NavLinks />
          </div>
        </nav>

        <main className="main-content">
          <Routes>
            <Route path="/" element={<Dashboard />} />
            <Route path="/details" element={<TableView />} />
          </Routes>
        </main>
      </div>
    </Router>
  );
}

export default App;

