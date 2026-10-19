import React, { useState } from 'react';
import { BusinessListing } from '../types';
import { X, Calculator, DollarSign, Percent, ShieldCheck, AlertTriangle } from 'lucide-react';

interface DealCalculatorModalProps {
  isOpen: boolean;
  onClose: () => void;
  initialListing?: BusinessListing | null;
}

export const DealCalculatorModal: React.FC<DealCalculatorModalProps> = ({
  isOpen,
  onClose,
  initialListing,
}) => {
  if (!isOpen) return null;

  const [purchasePrice, setPurchasePrice] = useState<number>(
    initialListing?.asking_price || 1200000
  );
  const [cashFlow, setCashFlow] = useState<number>(initialListing?.cash_flow || 380000);
  const [downPaymentPct, setDownPaymentPct] = useState<number>(10);
  const [interestRatePct, setInterestRatePct] = useState<number>(10.5);
  const [loanTermYears, setLoanTermYears] = useState<number>(10);

  // Calculations
  const downPaymentAmount = (purchasePrice * downPaymentPct) / 100;
  const loanAmount = Math.max(0, purchasePrice - downPaymentAmount);

  // Monthly payment calculation: M = P * [r(1+r)^n] / [(1+r)^n - 1]
  const monthlyRate = interestRatePct / 100 / 12;
  const numPayments = loanTermYears * 12;

  let monthlyDebtService = 0;
  if (monthlyRate > 0 && numPayments > 0 && loanAmount > 0) {
    monthlyDebtService =
      (loanAmount * (monthlyRate * Math.pow(1 + monthlyRate, numPayments))) /
      (Math.pow(1 + monthlyRate, numPayments) - 1);
  }

  const annualDebtService = monthlyDebtService * 12;
  const netCashFlow = cashFlow - annualDebtService;
  const dscr = annualDebtService > 0 ? cashFlow / annualDebtService : 99;
  const cashOnCash = downPaymentAmount > 0 ? (netCashFlow / downPaymentAmount) * 100 : 0;
  const priceToMultiple = cashFlow > 0 ? purchasePrice / cashFlow : 0;

  const formatMoney = (val: number) => `$${Math.round(val).toLocaleString()}`;

  return (
    <div className="fixed inset-0 z-50 overflow-y-auto bg-black/80 backdrop-blur-md flex items-center justify-center p-4">
      <div
        className="relative w-full max-w-2xl bg-slate-900 border border-slate-800 rounded-3xl overflow-hidden shadow-2xl p-6 sm:p-7 space-y-6"
        onClick={(e) => e.stopPropagation()}
      >
        {/* Header */}
        <div className="flex items-center justify-between pb-4 border-b border-slate-800">
          <div className="flex items-center gap-2.5">
            <div className="p-2 rounded-xl bg-teal-500/10 border border-teal-500/20 text-teal-400">
              <Calculator className="w-5 h-5" />
            </div>
            <div>
              <h2 className="text-lg font-bold text-white">
                SBA 7(a) Acquisition & ROI Simulator
              </h2>
              <p className="text-xs text-slate-400">
                Model cash-on-cash returns, leverage, and debt coverage
              </p>
            </div>
          </div>
          <button
            onClick={onClose}
            className="p-2 rounded-xl bg-slate-800 hover:bg-slate-700 text-slate-300 transition-all"
          >
            <X className="w-5 h-5" />
          </button>
        </div>

        {/* Inputs */}
        <div className="grid grid-cols-1 sm:grid-cols-2 gap-4">
          <div>
            <label className="text-xs font-bold text-slate-300 uppercase tracking-wider block mb-1">
              Purchase / Asking Price ($)
            </label>
            <input
              type="number"
              value={purchasePrice}
              onChange={(e) => setPurchasePrice(Number(e.target.value))}
              className="w-full px-3.5 py-2 bg-slate-950 border border-slate-800 rounded-xl text-sm font-semibold text-white focus:border-emerald-500"
            />
          </div>

          <div>
            <label className="text-xs font-bold text-slate-300 uppercase tracking-wider block mb-1">
              Annual Cash Flow / SDE ($)
            </label>
            <input
              type="number"
              value={cashFlow}
              onChange={(e) => setCashFlow(Number(e.target.value))}
              className="w-full px-3.5 py-2 bg-slate-950 border border-slate-800 rounded-xl text-sm font-semibold text-emerald-400 focus:border-emerald-500"
            />
          </div>

          <div>
            <div className="flex justify-between text-xs font-bold text-slate-300 uppercase tracking-wider mb-1">
              <span>Down Payment (%)</span>
              <span className="text-emerald-400 font-bold">{downPaymentPct}%</span>
            </div>
            <input
              type="range"
              min="5"
              max="50"
              step="5"
              value={downPaymentPct}
              onChange={(e) => setDownPaymentPct(Number(e.target.value))}
              className="w-full accent-emerald-500"
            />
          </div>

          <div>
            <div className="flex justify-between text-xs font-bold text-slate-300 uppercase tracking-wider mb-1">
              <span>Interest Rate (%)</span>
              <span className="text-cyan-400 font-bold">{interestRatePct}%</span>
            </div>
            <input
              type="range"
              min="5.0"
              max="15.0"
              step="0.25"
              value={interestRatePct}
              onChange={(e) => setInterestRatePct(Number(e.target.value))}
              className="w-full accent-cyan-500"
            />
          </div>
        </div>

        {/* Output Metrics Dashboard */}
        <div className="p-5 rounded-2xl bg-slate-950 border border-slate-800 space-y-4">
          <h3 className="text-xs font-bold text-slate-400 uppercase tracking-wider">
            Deal Projections
          </h3>

          <div className="grid grid-cols-2 sm:grid-cols-4 gap-3 text-center">
            <div className="p-3 rounded-xl bg-slate-900 border border-slate-800">
              <span className="text-[10px] uppercase font-bold text-slate-400 block">
                Required Equity
              </span>
              <span className="text-base font-extrabold text-white mt-0.5 block">
                {formatMoney(downPaymentAmount)}
              </span>
            </div>

            <div className="p-3 rounded-xl bg-slate-900 border border-slate-800">
              <span className="text-[10px] uppercase font-bold text-slate-400 block">
                Annual Loan Debt
              </span>
              <span className="text-base font-extrabold text-rose-400 mt-0.5 block">
                {formatMoney(annualDebtService)}
              </span>
            </div>

            <div className="p-3 rounded-xl bg-emerald-950/40 border border-emerald-800/40">
              <span className="text-[10px] uppercase font-bold text-emerald-400 block">
                Net Take-Home
              </span>
              <span className="text-base font-extrabold text-emerald-300 mt-0.5 block">
                {formatMoney(netCashFlow)}/yr
              </span>
            </div>

            <div className="p-3 rounded-xl bg-teal-950/40 border border-teal-800/40">
              <span className="text-[10px] uppercase font-bold text-teal-400 block">
                Cash-on-Cash ROI
              </span>
              <span className="text-base font-extrabold text-teal-300 mt-0.5 block">
                {cashOnCash.toFixed(1)}%
              </span>
            </div>
          </div>

          {/* DSCR Check */}
          <div className="pt-2 flex items-center justify-between text-xs px-2">
            <span className="text-slate-400">
              Debt Service Coverage Ratio (DSCR):{' '}
              <strong className="text-white">{dscr.toFixed(2)}x</strong>
            </span>
            <span
              className={`flex items-center gap-1 font-semibold ${
                dscr >= 1.25 ? 'text-emerald-400' : 'text-amber-400'
              }`}
            >
              {dscr >= 1.25 ? (
                <>
                  <ShieldCheck className="w-4 h-4" /> Bankable (SBA Qualified)
                </>
              ) : (
                <>
                  <AlertTriangle className="w-4 h-4" /> Tight Debt Coverage (&lt;1.25x)
                </>
              )}
            </span>
          </div>
        </div>

        {/* Footer */}
        <div className="flex justify-end pt-2">
          <button
            onClick={onClose}
            className="px-5 py-2.5 rounded-xl bg-slate-800 hover:bg-slate-700 text-slate-200 text-xs font-bold transition-all"
          >
            Done
          </button>
        </div>
      </div>
    </div>
  );
};
