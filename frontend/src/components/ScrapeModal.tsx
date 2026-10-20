import React, { useState, useEffect } from 'react';
import { triggerScraperJob, pollScraperStatus, clearListingsApi } from '../services/api';
import { ScrapeProgress } from '../types';
import {
  X,
  Sparkles,
  CheckCircle2,
  AlertCircle,
  Loader2,
  Globe,
  Layers,
  ArrowRight,
  CheckSquare,
  Square,
} from 'lucide-react';

interface ScrapeModalProps {
  isOpen: boolean;
  onClose: () => void;
  onScrapeComplete: () => void;
  availableSources: string[];
}

const ALL_SOURCES = [
  'BusinessesForSale',
  'BizBuySell',
  'Flippa',
  'Acquire.com',
  'Empire Flippers',
  'BusinessBroker.net',
  'FE International',
  'LoopNet',
];

export const ScrapeModal: React.FC<ScrapeModalProps> = ({
  isOpen,
  onClose,
  onScrapeComplete,
  availableSources,
}) => {
  if (!isOpen) return null;

  const sourcesList = availableSources.length > 0 ? availableSources : ALL_SOURCES;

  const [selectedSources, setSelectedSources] = useState<string[]>(sourcesList);
  const [keywords, setKeywords] = useState('');
  const [category, setCategory] = useState('');
  const [taskId, setTaskId] = useState<string | null>(null);
  const [progress, setProgress] = useState<ScrapeProgress | null>(null);
  const [isScraping, setIsScraping] = useState(false);
  const [clearFirst, setClearFirst] = useState(false);
  const [errorMsg, setErrorMsg] = useState<string | null>(null);

  const toggleSource = (source: string) => {
    setSelectedSources((prev) =>
      prev.includes(source) ? prev.filter((s) => s !== source) : [...prev, source]
    );
  };

  const handleSelectAll = () => {
    if (selectedSources.length === sourcesList.length) {
      setSelectedSources([]);
    } else {
      setSelectedSources([...sourcesList]);
    }
  };

  const handleStartScrape = async () => {
    if (selectedSources.length === 0) {
      setErrorMsg('Please select at least one marketplace platform to scrape.');
      return;
    }
    setErrorMsg(null);
    setIsScraping(true);
    setProgress(null);

    try {
      if (clearFirst) {
        await clearListingsApi(true);
      }
      const res = await triggerScraperJob(
        selectedSources,
        keywords.trim() || undefined,
        category.trim() || undefined
      );
      setTaskId(res.task_id);
    } catch (err: any) {
      setErrorMsg(err.message || 'Failed to start scraping task.');
      setIsScraping(false);
    }
  };

  useEffect(() => {
    if (!taskId || !isScraping) return;

    const interval = setInterval(async () => {
      try {
        const status = await pollScraperStatus(taskId);
        setProgress(status);

        if (status.status === 'completed' || status.status === 'failed') {
          setIsScraping(false);
          if (status.status === 'completed') {
            onScrapeComplete();
          }
        }
      } catch (e) {
        console.error('Polling error:', e);
      }
    }, 1000);

    return () => clearInterval(interval);
  }, [taskId, isScraping, onScrapeComplete]);

  return (
    <div className="fixed inset-0 z-50 overflow-y-auto bg-black/80 backdrop-blur-md flex items-center justify-center p-4">
      <div
        className="relative w-full max-w-2xl bg-slate-900 border border-slate-800 rounded-3xl overflow-hidden shadow-2xl p-6 sm:p-7 space-y-6"
        onClick={(e) => e.stopPropagation()}
      >
        {/* Header */}
        <div className="flex items-center justify-between pb-4 border-b border-slate-800">
          <div className="flex items-center gap-2.5">
            <div className="p-2 rounded-xl bg-emerald-500/10 border border-emerald-500/20 text-emerald-400">
              <Sparkles className="w-5 h-5" />
            </div>
            <div>
              <h2 className="text-lg font-bold text-white">Live Multi-Site Web Scraper</h2>
              <p className="text-xs text-slate-400">
                Harvest business listings across 8 online brokerages & marketplaces
              </p>
            </div>
          </div>
          {!isScraping && (
            <button
              onClick={onClose}
              className="p-2 rounded-xl bg-slate-800 hover:bg-slate-700 text-slate-300 transition-all"
            >
              <X className="w-5 h-5" />
            </button>
          )}
        </div>

        {/* Source Checkboxes */}
        {!isScraping && (
          <div className="space-y-4">
            <div className="flex items-center justify-between mb-1">
              <label className="text-xs font-bold text-slate-300 uppercase tracking-wider">
                Select Marketplaces to Query ({selectedSources.length}/{sourcesList.length})
              </label>
              <button
                type="button"
                onClick={handleSelectAll}
                className="text-xs text-emerald-400 hover:text-emerald-300 font-semibold"
              >
                {selectedSources.length === sourcesList.length ? 'Deselect All' : 'Select All'}
              </button>
            </div>

            <div className="grid grid-cols-2 sm:grid-cols-4 gap-2.5">
              {sourcesList.map((src) => {
                const isChecked = selectedSources.includes(src);
                return (
                  <button
                    key={src}
                    type="button"
                    onClick={() => toggleSource(src)}
                    className={`p-3 rounded-xl border text-left text-xs font-semibold flex flex-col justify-between h-20 transition-all ${
                      isChecked
                        ? 'bg-emerald-950/40 border-emerald-500/50 text-emerald-200 shadow-sm'
                        : 'bg-slate-950/60 border-slate-800 text-slate-400 hover:text-slate-200'
                    }`}
                  >
                    <div className="flex items-center justify-between w-full">
                      <span className="text-[10px] uppercase font-bold text-slate-500">Source</span>
                      <div
                        className={`w-4 h-4 rounded-md flex items-center justify-center border ${
                          isChecked
                            ? 'bg-emerald-500 border-emerald-400 text-slate-950'
                            : 'border-slate-700'
                        }`}
                      >
                        {isChecked && <CheckCircle2 className="w-3.5 h-3.5" />}
                      </div>
                    </div>
                    <span className="font-bold truncate text-slate-200">{src}</span>
                  </button>
                );
              })}
            </div>

            {/* Keyword Input */}
            <div className="pt-2">
              <label className="text-xs font-bold text-slate-300 uppercase tracking-wider block mb-1.5">
                Keyword Filter (Optional)
              </label>
              <input
                type="text"
                placeholder="e.g. 'Car Wash', 'SaaS', 'Plumbing', 'Amazon', 'Bakery'..."
                value={keywords}
                onChange={(e) => setKeywords(e.target.value)}
                className="w-full px-3.5 py-2.5 bg-slate-950 border border-slate-800 rounded-xl text-xs text-slate-200 focus:outline-none focus:border-emerald-500"
              />
            </div>

            {/* Clear Database Before Scraping Checkbox */}
            <label className="flex items-center gap-2.5 p-3 rounded-xl bg-slate-950/80 border border-slate-800 cursor-pointer hover:border-slate-700 transition-all">
              <input
                type="checkbox"
                checked={clearFirst}
                onChange={(e) => setClearFirst(e.target.checked)}
                className="rounded border-slate-700 text-emerald-500 focus:ring-emerald-500/30 bg-slate-800 w-4 h-4"
              />
              <div className="flex flex-col">
                <span className="text-xs text-slate-200 font-medium">
                  Clear old listings before scraping
                </span>
                <span className="text-[10px] text-slate-400">
                  Wipes stale unstarred listings so you start with fresh, real deals (saved watchlist deals are preserved)
                </span>
              </div>
            </label>

            {errorMsg && (
              <div className="p-3 rounded-xl bg-rose-950/40 border border-rose-800/50 text-rose-300 text-xs flex items-center gap-2">
                <AlertCircle className="w-4 h-4 shrink-0" />
                <span>{errorMsg}</span>
              </div>
            )}
          </div>
        )}

        {/* Live Progress Display */}
        {isScraping && progress && (
          <div className="space-y-4 py-2">
            <div className="flex items-center justify-between text-xs">
              <span className="font-semibold text-emerald-400 flex items-center gap-2">
                <Loader2 className="w-4 h-4 animate-spin" />
                {progress.message}
              </span>
              <span className="font-bold text-slate-200">{progress.progress}%</span>
            </div>

            {/* Progress Bar */}
            <div className="w-full h-2.5 bg-slate-950 rounded-full overflow-hidden border border-slate-800">
              <div
                className="h-full bg-gradient-to-r from-emerald-500 via-teal-400 to-cyan-400 transition-all duration-300"
                style={{ width: `${progress.progress}%` }}
              />
            </div>

            {/* Sources Live Status */}
            <div className="space-y-2 pt-2 max-h-52 overflow-y-auto pr-1">
              <span className="text-[11px] uppercase font-bold text-slate-400 tracking-wider">
                Live Source Crawler Status
              </span>
              <div className="grid grid-cols-2 gap-2">
                {Object.entries(progress.sources_status).map(([src, status]) => (
                  <div
                    key={src}
                    className="p-2.5 rounded-xl bg-slate-950/80 border border-slate-800 flex items-center justify-between text-xs"
                  >
                    <span className="font-medium text-slate-200 truncate mr-2">{src}</span>
                    <span
                      className={`text-[11px] font-semibold shrink-0 ${
                        status.includes('completed')
                          ? 'text-emerald-400'
                          : status === 'scraping'
                          ? 'text-amber-400 animate-pulse'
                          : 'text-slate-400'
                      }`}
                    >
                      {status}
                    </span>
                  </div>
                ))}
              </div>
            </div>
          </div>
        )}

        {/* Completed State */}
        {!isScraping && progress?.status === 'completed' && (
          <div className="p-4 rounded-2xl bg-emerald-950/30 border border-emerald-800/40 text-center space-y-2">
            <CheckCircle2 className="w-8 h-8 text-emerald-400 mx-auto" />
            <h4 className="text-sm font-bold text-emerald-200">Scraping Run Complete!</h4>
            <p className="text-xs text-slate-300">{progress.message}</p>
          </div>
        )}

        {/* Footer Actions */}
        <div className="flex items-center justify-end gap-3 pt-2">
          {!isScraping && (
            <>
              <button
                type="button"
                onClick={onClose}
                className="px-4 py-2 rounded-xl bg-slate-800 hover:bg-slate-700 text-slate-300 text-xs font-semibold"
              >
                Cancel
              </button>
              <button
                type="button"
                onClick={handleStartScrape}
                className="flex items-center gap-2 px-6 py-2.5 rounded-xl bg-gradient-to-r from-emerald-600 to-teal-600 hover:from-emerald-500 hover:to-teal-500 text-white text-xs font-bold shadow-lg shadow-emerald-950 active:scale-95 transition-all"
              >
                <Sparkles className="w-4 h-4" />
                <span>Scrape {selectedSources.length} Marketplaces</span>
              </button>
            </>
          )}
        </div>
      </div>
    </div>
  );
};
