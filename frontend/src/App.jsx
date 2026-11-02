import { BrowserRouter, Routes, Route } from 'react-router-dom'
import './App.css'
import { CustomerLayout, StaffLayout } from './Layout'
import Login from './customer/Login'
import Home from './customer/Home'
import Rewards from './customer/Rewards'
import Coupons from './customer/Coupons'
import History from './customer/History'
import StaffLogin from './staff/StaffLogin'
import Sale from './staff/Sale'
import Coupon from './staff/Coupon'

function App() {
  return (
    <BrowserRouter>
      <Routes>
        <Route path="login" element={<Login />} />
        <Route path="staff/login" element={<StaffLogin />} />
        <Route path="staff" element={<StaffLayout />}>
          <Route index element={<Sale />} />
          <Route path="coupon" element={<Coupon />} />
        </Route>
        <Route element={<CustomerLayout />}>
          <Route index element={<Home />} />
          <Route path="rewards" element={<Rewards />} />
          <Route path="coupons" element={<Coupons />} />
          <Route path="history" element={<History />} />
        </Route>
      </Routes>
    </BrowserRouter>
  )
}

export default App
