import { AdventurePlan } from '@/types/adventure';
import { Card, CardContent, CardHeader, CardTitle, CardDescription } from './ui/card';

interface AdventurePlanViewProps {
  plan: AdventurePlan;
}

export function AdventurePlanView({ plan }: AdventurePlanViewProps) {
  return (
    <div className="space-y-4">
      {plan.title && (
        <Card>
          <CardHeader>
            <CardTitle>{plan.title}</CardTitle>
            {plan.description && (
              <CardDescription>{plan.description}</CardDescription>
            )}
          </CardHeader>
        </Card>
      )}

      {plan.itinerary && (
        <Card>
          <CardHeader>
            <CardTitle>Itinerary</CardTitle>
          </CardHeader>
          <CardContent>
            <pre className="whitespace-pre-wrap text-sm">
              {typeof plan.itinerary === 'string'
                ? plan.itinerary
                : JSON.stringify(plan.itinerary, null, 2)}
            </pre>
          </CardContent>
        </Card>
      )}

      {plan.trails && plan.trails.length > 0 && (
        <Card>
          <CardHeader>
            <CardTitle>Trails</CardTitle>
          </CardHeader>
          <CardContent>
            <div className="space-y-2">
              {plan.trails.map((trail: any, i: number) => (
                <div key={i} className="border-l-4 border-primary pl-4">
                  <h4 className="font-semibold">{trail.name || trail.title}</h4>
                  {trail.description && (
                    <p className="text-sm text-muted-foreground">
                      {trail.description}
                    </p>
                  )}
                  {trail.difficulty && (
                    <span className="text-xs text-muted-foreground">
                      Difficulty: {trail.difficulty}
                    </span>
                  )}
                </div>
              ))}
            </div>
          </CardContent>
        </Card>
      )}

      {plan.gear_recommendations && plan.gear_recommendations.length > 0 && (
        <Card>
          <CardHeader>
            <CardTitle>Gear Recommendations</CardTitle>
          </CardHeader>
          <CardContent>
            <ul className="list-disc list-inside space-y-1">
              {plan.gear_recommendations.map((gear: any, i: number) => (
                <li key={i} className="text-sm">
                  {gear.name || gear.item || JSON.stringify(gear)}
                </li>
              ))}
            </ul>
          </CardContent>
        </Card>
      )}

      {plan.weather_info && (
        <Card>
          <CardHeader>
            <CardTitle>Weather Information</CardTitle>
          </CardHeader>
          <CardContent>
            <pre className="whitespace-pre-wrap text-sm">
              {typeof plan.weather_info === 'string'
                ? plan.weather_info
                : JSON.stringify(plan.weather_info, null, 2)}
            </pre>
          </CardContent>
        </Card>
      )}

      {plan.accommodation_info && plan.accommodation_info.length > 0 && (
        <Card>
          <CardHeader>
            <CardTitle>Accommodations</CardTitle>
          </CardHeader>
          <CardContent>
            <div className="space-y-2">
              {plan.accommodation_info.map((acc: any, i: number) => (
                <div key={i} className="text-sm">
                  <h4 className="font-semibold">{acc.name || acc.title}</h4>
                  {acc.description && (
                    <p className="text-muted-foreground">{acc.description}</p>
                  )}
                </div>
              ))}
            </div>
          </CardContent>
        </Card>
      )}
    </div>
  );
}

