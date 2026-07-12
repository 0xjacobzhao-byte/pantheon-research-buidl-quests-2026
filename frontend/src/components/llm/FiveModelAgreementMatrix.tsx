import type { AgreementMatrix } from "../../api";
import { verdictColor } from "./verdict";

/**
 * FiveModelAgreementMatrix — factor × provider heatmap of per-model verdicts,
 * colored by verdict. Rows are factors; columns are providers.
 */

export default function FiveModelAgreementMatrix({
  matrix,
  providers,
}: {
  matrix: AgreementMatrix;
  providers: string[];
}) {
  const cols =
    providers.length > 0
      ? providers
      : Array.from(
          new Set(matrix.factors.flatMap((f) => Object.keys(f.verdicts)))
        );

  return (
    <div className="agreement-matrix" data-testid="agreement-matrix">
      <div className="am-scroll">
        <table className="am-table">
          <thead>
            <tr>
              <th>Factor</th>
              {cols.map((p) => (
                <th key={p}>{p}</th>
              ))}
              <th>Agreement</th>
            </tr>
          </thead>
          <tbody>
            {matrix.factors.map((f) => (
              <tr key={f.factor}>
                <td className="am-factor">{f.factor.replace(/_/g, " ")}</td>
                {cols.map((p) => {
                  const v = f.verdicts[p];
                  return (
                    <td key={p} className="am-cell">
                      {v ? (
                        <span
                          className="am-chip"
                          style={{ backgroundColor: verdictColor(v) }}
                        >
                          {v}
                        </span>
                      ) : (
                        <span className="am-empty">—</span>
                      )}
                    </td>
                  );
                })}
                <td className="am-agree">
                  {!f.comparable ? (
                    <span className="am-na">n/a</span>
                  ) : f.agreement ? (
                    <span style={{ color: "var(--success)" }}>agree</span>
                  ) : (
                    <span style={{ color: "var(--warning)" }}>differ</span>
                  )}
                </td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
      <p className="am-summary">
        Agreement score:{" "}
        <strong>
          {matrix.agreement_score != null
            ? matrix.agreement_score.toFixed(2)
            : "n/a"}
        </strong>{" "}
        · {matrix.agreements}/{matrix.comparisons} comparable factors agree
      </p>
    </div>
  );
}
