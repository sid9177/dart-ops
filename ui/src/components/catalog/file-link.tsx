import type { RendererProps } from "@copilotkit/a2ui-renderer";

interface FileLinkProps {
  label: string;
  href: string;
}

export function FileLink({ props }: RendererProps<FileLinkProps>) {
  return (
    <a href={props.href} className="file-link" download>
      {props.label}
    </a>
  );
}