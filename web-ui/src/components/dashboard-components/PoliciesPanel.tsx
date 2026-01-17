import React, { useEffect, useMemo } from 'react';
import { Box, Tooltip, Typography, Paper } from '@mui/material';
import { useTranslation } from 'react-i18next';
import { PolicyType } from '../../../generated';
import { formatToShort } from '../../utils/sim-time-utils';
import { usePolicies } from '../../context/PoliciesContext';
import PrecisionManufacturingIcon from '@mui/icons-material/PrecisionManufacturing';
import FitnessCenterIcon from '@mui/icons-material/FitnessCenter';
import PaymentsIcon from '@mui/icons-material/Payments';
import ElderlyIcon from '@mui/icons-material/Elderly';
import { SvgIcon } from '@mui/material';

export interface PolicyInfo {
  type: PolicyType;
  color: string;
  icon: typeof SvgIcon;
  summary: string;
  name?: string; // Added name property
  effectUntil?: string;
}

const getPolicies = (): Pick<PolicyInfo, 'type' | 'color' | 'icon'>[] => {
  return [
    { type: 'FACTORY_MODERNIZATION', color: '#4caf50', icon: PrecisionManufacturingIcon },
    { type: 'GYM_IMPROVEMENT', color: '#2196f3', icon: FitnessCenterIcon },
    { type: 'LABOUR_SUBSIDIES', color: '#ff9800', icon: PaymentsIcon },
    { type: 'PENSION_SCHEME', color: '#9c27b0', icon: ElderlyIcon },
  ];
};

export const PoliciesPanel = () => {
  const { t } = useTranslation();

  const { policies: policyData, refreshPolicies } = usePolicies();

  useEffect(() => {
    if (!policyData) {
      refreshPolicies();
    }
  }, [refreshPolicies, policyData]);

  const policies = useMemo(
    () =>
      getPolicies().map((p) => {
        const activePolicy = policyData?.find((policy) => policy.type === p.type);

        const name = t(`policies.name.${p.type}`);
        const summary = t(`policies.summary.${p.type}`);

        return { ...p, summary, name, effectUntil: activePolicy ? activePolicy.effectUntil : undefined };
      }),
    [policyData],
  );

  return (
    <Box display="flex" flexDirection="row" gap={1} alignItems="center">
      {policies.map((p) => (
        <Tooltip
          key={p.type}
          title={
            <React.Fragment>
              <Typography sx={{ fontWeight: 700 }}>{p.name}</Typography>
              <Typography variant="body2">{p.summary}</Typography>
              {p.effectUntil ? (
                <Typography variant="caption" sx={{ display: 'block', marginTop: 0.5 }}>
                  {t('policies.effect_until', { effectUntil: formatToShort(p.effectUntil) })}
                </Typography>
              ) : null}
            </React.Fragment>
          }
          placement="top"
        >
          <Paper
            elevation={1}
            sx={{
              width: { xs: 40, xl: 50 },
              height: { xs: 40, xl: 50 },
              display: 'flex',
              alignItems: 'center',
              justifyContent: 'center',
              borderRadius: 1,
              border: !p.effectUntil ? '1px dashed rgba(0,0,0,0.2)' : undefined,
              opacity: !p.effectUntil ? 0.5 : 1,
              backgroundColor: !p.effectUntil ? '#121212' : p.color,
            }}
          >
            <p.icon style={{ fontSize: 26, color: !p.effectUntil ? '#bdbdbd' : '#121212' }} />
          </Paper>
        </Tooltip>
      ))}
    </Box>
  );
};

export default PoliciesPanel;
