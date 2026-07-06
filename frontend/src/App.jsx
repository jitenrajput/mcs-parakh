import { HashRouter, Routes, Route, Navigate } from 'react-router-dom'
import { I18nProvider } from './i18n'
import Launcher from './screens/Launcher'
import LenderDashboard from './screens/LenderDashboard'
import HealthCard from './screens/HealthCard'
import NewAssessment from './screens/NewAssessment'
import MsmeView from './screens/MsmeView'

export default function App() {
  return (
    <I18nProvider>
      <HashRouter>
        <Routes>
          <Route path="/" element={<Launcher />} />
          <Route path="/lender" element={<LenderDashboard />} />
          <Route path="/lender/:gstin" element={<HealthCard />} />
          <Route path="/assess/:gstin" element={<NewAssessment />} />
          <Route path="/msme/:gstin" element={<MsmeView />} />
          <Route path="*" element={<Navigate to="/" replace />} />
        </Routes>
      </HashRouter>
    </I18nProvider>
  )
}
