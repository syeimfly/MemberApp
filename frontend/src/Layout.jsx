import { NavLink, Navigate, Outlet } from 'react-router-dom'
import { getStaffKey, getToken } from './api'

const ICONS = {
  home: <path d="M3 11.5 12 4l9 7.5M5.5 10v9h13v-9" />,
  rewards: <path d="M20 12v9H4v-9M2 7h20v5H2V7Zm10 0v14M12 7H7.5a2.5 2.5 0 1 1 0-5C11 2 12 7 12 7Zm0 0h4.5a2.5 2.5 0 1 0 0-5C13 2 12 7 12 7Z" />,
  coupons: <path d="M3 8a2 2 0 0 0 0 4v0a2 2 0 0 1 0 4v2h18v-2a2 2 0 0 1 0-4v0a2 2 0 0 0 0-4V6H3v2Zm6-2v12" />,
  history: <path d="M12 7v5l3.5 2M21 12a9 9 0 1 1-9-9M21 5v4h-4" />,
  sale: <path d="M3 6h18l-1.5 9h-15L3 6Zm0 0-.5-2H1M8 19.5a1 1 0 1 0 0-2 1 1 0 0 0 0 2Zm9 0a1 1 0 1 0 0-2 1 1 0 0 0 0 2Z" />,
}

const CUSTOMER_TABS = [
  { to: '/', label: 'Home', end: true, icon: 'home' },
  { to: '/rewards', label: 'Rewards', icon: 'rewards' },
  { to: '/coupons', label: 'Coupons', icon: 'coupons' },
  { to: '/history', label: 'History', icon: 'history' },
]

const STAFF_TABS = [
  { to: '/staff', label: 'Sale', end: true, icon: 'sale' },
  { to: '/staff/coupon', label: 'Coupon', icon: 'coupons' },
]

function Shell({ tabs, title }) {
  return (
    <div className="app-shell">
      <header className="app-header">
        <span className="app-title">{title}</span>
      </header>
      <main className="app-content">
        <Outlet />
      </main>
      <nav className="bottom-nav">
        {tabs.map((tab) => (
          <NavLink
            key={tab.to}
            to={tab.to}
            end={tab.end}
            className={({ isActive }) => 'nav-tab' + (isActive ? ' active' : '')}
          >
            <svg className="nav-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="1.8" strokeLinecap="round" strokeLinejoin="round">
              {ICONS[tab.icon]}
            </svg>
            <span>{tab.label}</span>
          </NavLink>
        ))}
      </nav>
    </div>
  )
}

export function CustomerLayout() {
  if (!getToken()) return <Navigate to="/login" replace />
  return <Shell tabs={CUSTOMER_TABS} title="MemberApp" />
}

export function StaffLayout() {
  if (!getStaffKey()) return <Navigate to="/staff/login" replace />
  return <Shell tabs={STAFF_TABS} title="MemberApp Staff" />
}
